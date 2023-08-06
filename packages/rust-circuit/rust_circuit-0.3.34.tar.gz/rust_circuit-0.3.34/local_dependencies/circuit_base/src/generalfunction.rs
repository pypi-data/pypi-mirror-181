use std::{fmt, iter::zip};

use anyhow::{anyhow, bail, Context, Result};
use macro_rules_attribute::apply;
use once_cell::sync::Lazy;
use pyo3::{
    exceptions::PyValueError,
    once_cell::{GILLazy, GILLazyPy},
    prelude::{PyAny, *},
    types::PyTuple,
};
use rand::Rng;
use regex::Regex;
use rr_util::{
    py_types::{assert_tensors_close, ExtraPySelfOps, PyShape, Tensor, PY_UTILS},
    pycall, python_error_exception, simple_from,
    tensor_util::{
        check_canon_idxs, MiscInputError, Shape, TorchDeviceDtype, TorchDeviceDtypeOp, TorchDtype,
    },
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use thiserror::Error;
use uuid::uuid;

use crate::{
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeComputeInfoImpl, CircuitNodeHashItems},
    circuit_utils::OperatorPriority,
    new_rc_unwrap,
    prelude::*,
    Array, CachedCircuitInfo, HashBytes, PyCircuitBase,
};

macro_rules! gf_gen {
    ($(($name:ident, $($t:tt)*)),* $(,)?) => {
        pub const BASIC_SPEC_ITEMS: &'static [(&'static str, u8, u8)] = &[
            $(
                gf_gen!(@item $name, $($t)*),
            )*
        ];

        $(
        #[pyfunction]
        pub fn $name(circuit: CircuitRc, name: Option<String>) -> Result<GeneralFunction> {
            GeneralFunction::new_by_name(vec![circuit], stringify!($name).to_owned(), name)
        }
        )*

        pub fn register(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
            $(
            m.add_function(wrap_pyfunction!($name, m)?)?;
            )*
            Ok(())
        }
    };
    (@item $name:ident, $non_b:expr, $rem:expr $(,)?) => {
        (stringify!($name), $non_b, $rem)
    };
    (@item $name:ident, $non_b:expr $(,)?) => {
        (stringify!($name), $non_b, 0)
    };
}

gf_gen!(
    (sigmoid, 0),
    (tanh, 0),
    (rsqrt, 0),
    (gelu, 0),
    (relu, 0),
    (step, 0),
    (reciprocal, 0),
    (log_exp_p_1, 0),
    (gaussian_pdf, 0),
    (gaussian_cdf, 0),
    (softmax, 1),
    (log_softmax, 1),
    // (q_from_qr, 2), // TODO: this requires first dim > second dim!
    (min, 0, 1),
    (max, 0, 1),
    (last_dim_size, 0, 1),
);

static SPECS: GILLazy<HashMap<String, GeneralFunctionSpec>> = GILLazy::new(|| {
    BASIC_SPEC_ITEMS
        .iter()
        .cloned()
        .map(|(name, num_non_batchable_output_dims, removed_from_end)| {
            let name = name.to_owned();
            (
                name.clone(),
                GeneralFunctionSimpleSpec {
                    name,
                    num_non_batchable_output_dims,
                    removed_from_end,
                }
                .into(),
            )
        })
        .collect()
});

pub const OFFICIAL_GENERALFUNCTION_INVERSES: [(&str, &str); 1] = [("reciprocal", "reciprocal")];

/// GeneralFunctionSpec contains all needed info about function, and is the same on all instances with the same function
/// how batchability works: input_batchability is a mask indicating which inputs support batching. if none do, there is no batching.
/// the number of non batchable dims in output, starting from end, is num_non_batchable_output_dims.
pub trait SpecTrait: fmt::Debug + ToPyObject {
    fn compute_hash(&self) -> HashBytes;
    fn function(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor>;
    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo>;
    // fn has_jacobian(&self) -> Result<bool>;
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>>;
    fn name(&self) -> String;
    fn is_official(&self) -> bool {
        false
    }
    fn serialize(&self) -> Result<Option<String>>;
    fn get_device_dtype_override(
        &self,
        _device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Option<Result<TorchDeviceDtypeOp>> {
        None
    } // returning None means use normal device_dtype inheritance. if Some, then error if dtypes are incorrect and dtype if correct
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionShapeInfo {
    #[pyo3(set)]
    pub shape: Shape,
    #[pyo3(get, set)]
    pub num_non_batchable_output_dims: u8,
    #[pyo3(get, set)]
    pub input_batchability: Vec<bool>,
}

#[pymethods]
impl GeneralFunctionShapeInfo {
    #[getter]
    fn shape(&self) -> PyShape {
        PyShape(self.shape.clone())
    }

    /// no checking done here, we assume valid
    #[new]
    pub fn new(
        shape: Shape,
        num_non_batchable_output_dims: u8,
        input_batchability: Vec<bool>,
    ) -> Self {
        Self {
            shape,
            num_non_batchable_output_dims,
            input_batchability,
        }
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionSimpleSpec {
    #[pyo3(get)]
    name: String,
    #[pyo3(get)]
    num_non_batchable_output_dims: u8,
    #[pyo3(get)]
    removed_from_end: u8,
}

simple_from!(|x: GeneralFunctionSimpleSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::Simple(x)
});

impl ToPyObject for GeneralFunctionSimpleSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

#[pyfunction]
pub fn get_shape_info_simple(
    shapes: Vec<Shape>,
    num_non_batchable_output_dims: Option<u8>,
    removed_from_end: Option<u8>,
) -> Result<GeneralFunctionShapeInfo> {
    GeneralFunctionSimpleSpec {
        name: "".to_owned(),
        num_non_batchable_output_dims: num_non_batchable_output_dims.unwrap_or(0),
        removed_from_end: removed_from_end.unwrap_or(0),
    }
    .get_shape_info(&shapes)
}

#[pymethods]
impl GeneralFunctionSimpleSpec {
    fn get_function(&self) -> PyObject {
        PY_UTILS.generalfunctions[&self.name].clone()
    }
}

impl GeneralFunctionSimpleSpec {}

impl SpecTrait for GeneralFunctionSimpleSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("f1f0bc63-f390-412b-9e98-74ce65911006").as_bytes()); // uuid for SimpleSpec
        hasher.update(self.name.as_bytes()); // names are unique
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            Ok(self
                .get_function()
                .call(
                    py,
                    PyTuple::new(py, tensors.iter().map(|x| x.clone().into_py(py))),
                    None,
                )
                .context(format!("evaluate function {}", self.name))?
                .extract(py)
                .unwrap())
        })
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        if shapes.len() != 1 {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 1
            });
        }
        if (shapes[0].len() as u8) < self.num_non_batchable_output_dims + self.removed_from_end {
            bail!(GeneralFunctionShapeError::NDimTooSmall {
                ndim: shapes[0].len(),
                num_non_batchable_output_dims: self.num_non_batchable_output_dims,
                removed_from_end: self.removed_from_end
            });
        }
        Ok(GeneralFunctionShapeInfo {
            shape: shapes[0][..shapes[0].len() - self.removed_from_end as usize]
                .iter()
                .cloned()
                .collect(),
            num_non_batchable_output_dims: self.num_non_batchable_output_dims,
            input_batchability: vec![true].into_iter().collect(),
        })
    }

    // fn has_jacobian(&self) -> Result<bool> {
    //     Ok(self.get_jacobians.is_some())
    // }
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>> {}

    fn name(&self) -> String {
        self.name.clone()
    }
    fn is_official(&self) -> bool {
        true
    }
    fn serialize(&self) -> Result<Option<String>> {
        Ok(Some(self.name.clone()))
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionIndexSpec {
    #[pyo3(get)]
    index_dim: i64,
    #[pyo3(get)]
    batch_x: bool,
    #[pyo3(get)]
    check_index_ints: bool,
}

simple_from!(|x: GeneralFunctionIndexSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::Index(x)
});

impl ToPyObject for GeneralFunctionIndexSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

impl SpecTrait for GeneralFunctionIndexSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(uuid!("442fde55-a1b7-4a69-98ff-bd40d7030ef2").as_bytes()); // uuid for Index
        hasher.update(&self.index_dim.to_le_bytes());
        hasher.update(&[self.batch_x as u8, self.check_index_ints as u8]);
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            Ok(PY_UTILS
                .gen_index_function
                .call(
                    py,
                    PyTuple::new(
                        py,
                        tensors
                            .iter()
                            .map(|x| x.clone().into_py(py))
                            .chain([
                                self.index_dim.into_py(py),
                                self.batch_x.into_py(py),
                                self.check_index_ints.into_py(py),
                            ])
                            .collect::<Vec<_>>(),
                    ),
                    None,
                )
                .context("evaluate gen index")?
                .extract(py)
                .unwrap())
        })
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        let (x_shape, index_shape) = if let [x_shape, index_shape] = shapes {
            (x_shape, index_shape)
        } else {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 2
            });
        };

        // TODO: improve errors as needed
        let get_err = || GeneralFunctionShapeError::IndexShapeInvalid {
            x_shape: x_shape.clone(),
            index_shape: index_shape.clone(),
            batch_x: self.batch_x,
        };

        if self.batch_x {
            let prefix_len = index_shape.len();
            if prefix_len >= x_shape.len() {
                // condition to ensure that suffix len >= 1
                bail!(get_err())
            }

            if &x_shape[..prefix_len] != &index_shape[..] {
                bail!(get_err())
            }

            let suffix_len = x_shape.len() - prefix_len;
            assert!(suffix_len >= 1);
            let final_index_dim = check_canon_idxs(suffix_len, &[self.index_dim])
                .context("index dim out of bounds for 'suffix'")?[0]
                + prefix_len;

            Ok(GeneralFunctionShapeInfo {
                shape: x_shape[..final_index_dim]
                    .iter()
                    .chain(&x_shape[final_index_dim + 1..])
                    .cloned()
                    .collect(),
                num_non_batchable_output_dims: (suffix_len - 1) as u8, // sub 1 for indexed
                input_batchability: vec![true, true].into_iter().collect(),
            })
        } else {
            let index_dim = check_canon_idxs(x_shape.len(), &[self.index_dim])
                .context("index dim out of bounds for x_shape")?[0];

            Ok(GeneralFunctionShapeInfo {
                shape: index_shape
                    .iter()
                    .chain(&x_shape[..index_dim])
                    .chain(&x_shape[index_dim + 1..])
                    .cloned()
                    .collect(),
                num_non_batchable_output_dims: (x_shape.len() - 1) as u8, // sub 1 for indexed
                input_batchability: vec![false, true].into_iter().collect(),
            })
        }
    }

    // fn has_jacobian(&self) -> Result<bool> {
    //     Ok(self.get_jacobians.is_some())
    // }
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>> {}
    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Option<Result<TorchDeviceDtypeOp>> {
        if let Some(dev1) = device_dtypes[0].device && let Some(dev2) = device_dtypes[1].device && dev1!=dev2{
            return Some(Err(MiscInputError::ChildrenMultipleDevices { a: device_dtypes[0].device, b: device_dtypes[1].device}.into()))
        }
        if let Some(dtype) = device_dtypes[1].dtype && dtype != TorchDtype::int64 {
            return Some(Err(MiscInputError::IndexDtypeNotI64 {}.into()));
        }
        Some(Ok(device_dtypes[0]))
    }
    fn name(&self) -> String {
        format!(
            "gen_index_at_{}{}{}",
            self.index_dim,
            if self.batch_x { "_batch_x" } else { "" },
            if self.check_index_ints { "_c" } else { "" }
        )
    }
    fn is_official(&self) -> bool {
        true
    }
    fn serialize(&self) -> Result<Option<String>> {
        Ok(Some(self.name()))
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct GeneralFunctionSetDDSpec {
    #[pyo3(get)]
    input_required_compatibility: TorchDeviceDtypeOp,
    #[pyo3(get)]
    output: TorchDeviceDtypeOp,
}

simple_from!(|x: GeneralFunctionSetDDSpec| -> GeneralFunctionSpec {
    GeneralFunctionSpec::SetDD(x)
});

impl ToPyObject for GeneralFunctionSetDDSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

impl SpecTrait for GeneralFunctionSetDDSpec {
    fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        self.input_required_compatibility.hash(&mut hasher);
        self.output.hash(&mut hasher);
        *hasher.finalize().as_bytes()
    }

    fn function(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        pycall!(
            PY_UTILS.cast_tensor,
            (tensors[0].clone(), self.output),
            anyhow
        )
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        if shapes.len() != 1 {
            bail!(GeneralFunctionShapeError::WrongNumShapes {
                got: shapes.len(),
                expected: 1
            });
        }
        Ok(GeneralFunctionShapeInfo {
            shape: shapes[0].clone(),
            num_non_batchable_output_dims: 0,
            input_batchability: vec![true].try_into().unwrap(),
        })
    }
    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Option<Result<TorchDeviceDtypeOp>> {
        Some(
            self.input_required_compatibility
                .combine(device_dtypes[0])
                .map_err(|_e| {
                    MiscInputError::CastIncompatibleDeviceDtype {
                        required: self.input_required_compatibility,
                        actual: device_dtypes[0],
                    }
                    .into()
                })
                .map(|_| self.output.override_other(device_dtypes[0])),
        )
    }

    // fn has_jacobian(&self) -> Result<bool> {
    //     Ok(self.get_jacobians.is_some())
    // }
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>> {}

    fn name(&self) -> String {
        format!(
            "cast_{:?}_{:?}",
            self.input_required_compatibility, self.output
        )
    }
    fn serialize(&self) -> Result<Option<String>> {
        Ok(Some(self.name()))
    }
}

#[derive(Clone)]
pub struct PyWrap {
    ob: PyObject,
    hash: HashBytes,
    name: String,
    path: Option<String>,
}

impl fmt::Debug for PyWrap {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("PyWrap")
            .field("ob", &self.ob)
            .field("name", &self.name)
            .field("path", &self.path)
            .finish_non_exhaustive()
    }
}

simple_from!(|x: PyWrap| -> GeneralFunctionSpec { GeneralFunctionSpec::Py(Box::new(x)) });

pub static PY_WRAP_BASE: GILLazyPy<PyObject> = GILLazyPy::new_py(|py| {
    let py_part = PyModule::from_code(
        py,
        include_str!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/py_general_function_spec.py"
        )),
        concat!(env!("CARGO_MANIFEST_DIR"), "/py_general_function_spec.py"),
        "py_general_function_spec",
    )
    .unwrap();

    let get = |s: &str| py_part.getattr(s).unwrap().into();

    get("GeneralFunctionSpecBase")
});

impl<'source> pyo3::FromPyObject<'source> for Box<PyWrap> {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        let ob: PyObject = ob.into();
        let mut hasher = blake3::Hasher::new();
        if !Python::with_gil(|py| ob.as_ref(py).is_instance(PY_WRAP_BASE.as_ref(py)))
            .context("is instance failed???")?
        {
            let err: anyhow::Error = ConstructError::GeneralFunctionPyNotInstance { ob }.into();
            return Err(err.into());
        }

        hasher.update(uuid!("de3124ee-154c-4da8-bdb3-b7496ae6223c").as_bytes()); // uuid for PyWrap
        let bytes: Vec<u8> = Python::with_gil(|py| -> Result<_> {
            Ok(ob.call_method0(py, "compute_hash_bytes")?.extract(py)?)
        })?;
        hasher.update(&bytes);

        let name: String =
            Python::with_gil(|py| -> Result<_> { Ok(ob.getattr(py, "name")?.extract(py)?) })?;

        if name.contains(" at ") {
            return Err(anyhow!("Function names can't contain the substring ` at ` because it could interfere with parsing.").into());
        }

        let path: Option<String> =
            Python::with_gil(|py| -> Result<_> { Ok(ob.getattr(py, "path")?.extract(py)?) })?;

        if let Some(p) = &path && (!p.starts_with("/") || !p.contains(".py:")) {
            return Err(anyhow!("Function path of the form /dir/sub_dir/.../file.py:MyCustomSpec. (relative to rrfs)").into());
        }

        Ok(Box::new(PyWrap {
            name,
            path,
            ob,
            hash: *hasher.finalize().as_bytes(),
        }))
    }
}

impl ToPyObject for Box<PyWrap> {
    fn to_object(&self, _py: Python<'_>) -> PyObject {
        self.ob.clone()
    }
}

impl SpecTrait for Box<PyWrap> {
    fn compute_hash(&self) -> HashBytes {
        self.hash
    }
    fn function(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            Ok(self
                .ob
                .call_method1(
                    py,
                    "function",
                    PyTuple::new(py, tensors.iter().map(|x| x.clone().into_py(py))),
                )?
                .extract(py)?)
        })
    }

    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        Python::with_gil(|py| {
            Ok(self
                .ob
                .call_method1(
                    py,
                    "get_shape_info",
                    // PyShape here is important!
                    PyTuple::new(py, shapes.iter().map(|x| PyShape(x.clone()).into_py(py))),
                )?
                .extract(py)?)
        })
    }
    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Option<Result<TorchDeviceDtypeOp>> {
        let resulty: Result<Option<TorchDeviceDtypeOp>> = Python::with_gil(|py| {
            Ok(self
                .ob
                .call_method1(
                    py,
                    "get_device_dtype_override",
                    PyTuple::new(
                        py,
                        device_dtypes
                            .iter()
                            .map(|x| x.into_py(py))
                            .collect::<Vec<_>>(),
                    ),
                )?
                .extract(py)?)
        });
        if let Err(e) = resulty {
            return Some(Err(e));
        }
        return resulty.unwrap().map(|x| Ok(x));
    }
    fn name(&self) -> String {
        self.name.clone()
    }
    fn serialize(&self) -> Result<Option<String>> {
        match &self.path {
            Some(p) => Ok(Some(format!("{} at {}", &self.name, p))),
            None => bail!(anyhow!(format!(
                "Can't serialize function {}: no path given",
                &self.name
            ))),
        }
    }
}

#[derive(Debug, Clone, FromPyObject)]
pub enum GeneralFunctionSpec {
    Simple(GeneralFunctionSimpleSpec),
    Index(GeneralFunctionIndexSpec),
    SetDD(GeneralFunctionSetDDSpec),
    Py(Box<PyWrap>), // boxed bc it was long pole for Circuit size
}

impl GeneralFunctionSpec {
    #[inline]
    fn as_trait_obj(&self) -> &dyn SpecTrait {
        match self {
            Self::Simple(x) => x,
            Self::Index(x) => x,
            Self::SetDD(x) => x,
            Self::Py(x) => x,
        }
    }
}

impl ToPyObject for GeneralFunctionSpec {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.as_trait_obj().to_object(py)
    }
}
impl IntoPy<PyObject> for GeneralFunctionSpec {
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.to_object(py)
    }
}

impl SpecTrait for GeneralFunctionSpec {
    fn compute_hash(&self) -> HashBytes {
        self.as_trait_obj().compute_hash()
    }
    fn function(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        self.as_trait_obj().function(tensors, device_dtype)
    }
    fn get_shape_info(&self, shapes: &[Shape]) -> Result<GeneralFunctionShapeInfo> {
        self.as_trait_obj().get_shape_info(shapes)
    }
    fn get_device_dtype_override(
        &self,
        device_dtypes: &[TorchDeviceDtypeOp],
    ) -> Option<Result<TorchDeviceDtypeOp>> {
        self.as_trait_obj().get_device_dtype_override(device_dtypes)
    }
    // fn has_jacobian(&self) -> Result<bool>;
    // fn get_jacobians(&self, func: &GeneralFunction) -> Result<Option<Vec<Circuit>>>;
    fn name(&self) -> String {
        self.as_trait_obj().name()
    }
    fn is_official(&self) -> bool {
        self.as_trait_obj().is_official()
    }
    fn serialize(&self) -> Result<Option<String>> {
        self.as_trait_obj().serialize()
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct GeneralFunction {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    #[pyo3(get)]
    pub spec: GeneralFunctionSpec,
    info: CachedCircuitInfo,
    name: Option<String>,
    #[pyo3(get)]
    pub num_non_batchable_output_dims: u8,
    pub input_batchability: Vec<bool>,
}

impl GeneralFunction {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        nodes: Vec<CircuitRc>,
        spec: GeneralFunctionSpec,
        name: Option<String>,
    ) -> Result<Self> {
        let shapes = nodes
            .iter()
            .map(|x| x.shape().clone())
            .collect::<Vec<Shape>>();

        let GeneralFunctionShapeInfo {
            shape,
            num_non_batchable_output_dims,
            input_batchability,
        } = spec.get_shape_info(&shapes).with_context(|| {
            format!(
                "failed to compute shape info in new with spec={:?} input_shapes={:?}",
                spec,
                nodes
                    .iter()
                    .map(|x| x.shape().clone())
                    .collect::<Vec<Shape>>()
            )
        })?;

        let mut out = Self {
            nodes,
            spec,
            name,
            info: Default::default(),
            num_non_batchable_output_dims,
            input_batchability,
        };
        out.info.shape = shape; // set shape so we only compute once
        out.initial_init_info()
    }

    pub fn is_batchable(&self) -> bool {
        self.input_batchability.iter().any(|x| *x)
    }
}

circuit_node_extra_impl!(GeneralFunction, self_hash_default);

impl CircuitNodeComputeInfoImpl for GeneralFunction {
    fn compute_shape(&self) -> Shape {
        self.info.shape.clone() // set in try new!
    }

    fn device_dtype_override(&self) -> Option<Result<TorchDeviceDtypeOp>> {
        self.spec.get_device_dtype_override(
            &self
                .nodes
                .iter()
                .map(|x| x.info().device_dtype)
                .collect::<Vec<_>>(),
        )
    }
}

impl CircuitNodeHashItems for GeneralFunction {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        hasher.update(&self.spec.compute_hash());
    }
}

impl CircuitNode for GeneralFunction {
    circuit_node_auto_impl!("3c655670-b352-4a5f-891c-0d7160609341");

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ.clone()))
                .collect::<Result<Vec<_>, _>>()?,
            self.spec.clone(),
            self.name.clone(),
        )
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let num_batchable_axes = self.info().rank() as u8 - self.num_non_batchable_output_dims;
        zip(&self.nodes, &self.input_batchability)
            .map(|(child, batchable)| {
                if !batchable {
                    vec![None; child.info().rank()]
                } else {
                    (0..child.info().rank())
                        .map(|i| match i < num_batchable_axes as usize {
                            true => Some(i),
                            false => None,
                        })
                        .collect()
                }
            })
            .collect()
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        self.spec.function(tensors, device_dtype)
    }
}

impl CircuitNodeAutoName for GeneralFunction {
    const PRIORITY: OperatorPriority = OperatorPriority::Function {};

    fn auto_name(&self) -> Option<String> {
        // Never any parenthesis, so we don't even care checking if we need to add some
        // but check out children_names_with_maybe_paren if you change the syntax of the general function
        if self.children().any(|x| x.name().is_none()) {
            None
        } else {
            Some(
                self.spec.name().clone()
                    + "("
                    + &self
                        .children()
                        .map(|x| Self::shorten_child_name(x.name().unwrap()))
                        .collect::<Vec<String>>()
                        .join(", ")
                    + ")",
            )
        }
    }
}

#[pymethods]
impl GeneralFunction {
    #[new]
    #[args(nodes = "*", spec, name = "None")]
    fn new_py(
        nodes: Vec<CircuitRc>,
        spec: GeneralFunctionSpec,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<GeneralFunction>> {
        let out = GeneralFunction::try_new(nodes, spec, name)?;

        Ok(out.into_init())
    }

    #[staticmethod]
    #[args(nodes = "*", spec_name, name = "None")]
    pub fn new_from_parse(
        nodes: Vec<CircuitRc>,
        parse_string: String,
        name: Option<String>,
    ) -> Result<Self> {
        if parse_string.contains(" at ") {
            let mut split = parse_string.splitn(2, " at ");
            let name = convert_op_str_to_format_err(split.next(), &parse_string)?;
            let path = convert_op_str_to_format_err(split.next(), &parse_string)?;

            Self::new_by_path(nodes, path, Some(name))
        } else {
            Self::new_by_name(nodes, parse_string, name)
        }
    }

    #[staticmethod]
    #[args(nodes = "*", spec_name, name = "None")]
    pub fn new_by_name(
        nodes: Vec<CircuitRc>,
        spec_name: String,
        name: Option<String>,
    ) -> Result<Self> {
        Self::new_by_name_op(nodes, spec_name.clone(), name)?
            .ok_or(ConstructError::UnknownGeneralFunction { spec_name }.into())
    }

    #[staticmethod]
    #[args(nodes = "*", spec_name, name = "None")]
    pub fn new_by_name_op(
        nodes: Vec<CircuitRc>,
        spec_name: String,
        name: Option<String>,
    ) -> Result<Option<Self>> {
        // parse index case
        static RE: Lazy<Regex> =
            Lazy::new(|| Regex::new(r"^gen_index_at_(-?\d+)(_batch_x)?(_c)?$").unwrap());
        let spec = if let Some(re_captures) = RE.captures(&spec_name) {
            let index_dim = re_captures
                .get(1)
                .unwrap()
                .as_str()
                .parse()
                .context("failed to parse index_dim for gen_index_at")?;
            let batch_x = re_captures.get(2).is_some();
            let check_index_ints = re_captures.get(3).is_some();
            GeneralFunctionIndexSpec {
                index_dim,
                batch_x,
                check_index_ints,
            }
            .into()
        } else if let Some(spec) = SPECS.get(&spec_name) {
            spec.clone()
        } else {
            return Ok(None);
        };

        GeneralFunction::try_new(nodes, spec, name).map(Some)
    }

    #[staticmethod]
    #[args(nodes = "*", path, name = "None")]
    pub fn new_by_path(nodes: Vec<CircuitRc>, path: String, name: Option<String>) -> Result<Self> {
        let mut split = path.splitn(2, ":");
        let file_path = convert_op_str_to_format_err(split.next(), &path)?;
        let spec_name = convert_op_str_to_format_err(split.next(), &path)?;

        let spec: GeneralFunctionSpec =
            Python::with_gil(|py| -> Result<GeneralFunctionSpec, pyo3::PyErr> {
                let rrfs_dir = py
                    .import("interp.tools.rrfs")?
                    .getattr("RRFS_DIR")?
                    .extract::<String>()?;

                // adapted from https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path

                let importlib_util = py.import("importlib.util")?;
                let spec = importlib_util.call_method1(
                    "spec_from_file_location",
                    ("user_funcs", rrfs_dir + &file_path),
                )?;
                let function_spec_module =
                    importlib_util.call_method1("module_from_spec", (spec,))?;
                spec.getattr("loader")?
                    .call_method1("exec_module", (function_spec_module,))?;
                let spec_cls = function_spec_module.getattr(&*spec_name)?;
                spec_cls.call0()?.extract()
            })?;

        GeneralFunction::try_new(nodes, spec, name)
    }

    #[staticmethod]
    #[args(batch_x = "false", check_index_ints = "true", name = "None")]
    pub fn gen_index(
        x: CircuitRc,
        index: CircuitRc,
        index_dim: i64,
        batch_x: bool,
        check_index_ints: bool,
        name: Option<String>,
    ) -> Result<Self> {
        let spec = GeneralFunctionIndexSpec {
            index_dim,
            batch_x,
            check_index_ints,
        }
        .into();
        Self::try_new(vec![x, index], spec, name)
    }
    #[staticmethod]
    #[args(
        input_required_compatibility = "Default::default()",
        output = "Default::default()",
        name = "None"
    )]
    pub fn new_cast(
        x: CircuitRc,
        input_required_compatibility: TorchDeviceDtypeOp,
        output: TorchDeviceDtypeOp,
        name: Option<String>,
    ) -> Result<Self> {
        let spec = GeneralFunctionSetDDSpec {
            input_required_compatibility,
            output,
        }
        .into();
        Self::try_new(vec![x], spec, name)
    }
}

/// I now think this maybe should have been written in python.
/// Not to bad to port I guess...
#[pyclass]
pub struct GeneralFunctionSpecTester {
    #[pyo3(set, get)]
    pub samples_per_batch_dims: usize,
    #[pyo3(set, get)]
    pub base_shapes_samples: usize,
    #[pyo3(set, get)]
    pub min_frac_successful: f64,
    #[pyo3(set, get)]
    pub min_frac_checked_batch: f64,
    #[pyo3(set, get)]
    pub start_num_inputs: usize,
    #[pyo3(set, get)]
    pub end_num_inputs: usize,
    #[pyo3(set, get)]
    pub start_ndim: usize,
    #[pyo3(set, get)]
    pub end_ndim: usize,
    #[pyo3(set, get)]
    pub start_shape_num: usize,
    #[pyo3(set, get)]
    pub end_shape_num: usize,
    #[pyo3(set, get)]
    pub test_with_rand: bool,
    #[pyo3(set, get)]
    pub randn_size_cap: usize,
}

impl Default for GeneralFunctionSpecTester {
    fn default() -> Self {
        Self {
            samples_per_batch_dims: 3,
            base_shapes_samples: 100,
            min_frac_successful: 0.1,
            min_frac_checked_batch: 0.1,
            start_num_inputs: 0,
            end_num_inputs: 5,
            start_ndim: 0,
            end_ndim: 10,
            start_shape_num: 0,
            end_shape_num: 10,
            test_with_rand: true,
            randn_size_cap: 1024 * 16,
        }
    }
}

#[pymethods]
impl GeneralFunctionSpecTester {
    #[new]
    #[args(
        samples_per_batch_dims = "GeneralFunctionSpecTester::default().samples_per_batch_dims",
        base_shapes_samples = "GeneralFunctionSpecTester::default().base_shapes_samples",
        min_frac_successful = "GeneralFunctionSpecTester::default().min_frac_successful",
        min_frac_checked_batch = "GeneralFunctionSpecTester::default().min_frac_checked_batch",
        start_num_inputs = "GeneralFunctionSpecTester::default().start_num_inputs",
        end_num_inputs = "GeneralFunctionSpecTester::default().end_num_inputs",
        start_ndim = "GeneralFunctionSpecTester::default().start_ndim",
        end_ndim = "GeneralFunctionSpecTester::default().end_ndim",
        start_shape_num = "GeneralFunctionSpecTester::default().start_shape_num",
        end_shape_num = "GeneralFunctionSpecTester::default().end_shape_num",
        test_with_rand = "GeneralFunctionSpecTester::default().test_with_rand",
        randn_size_cap = "GeneralFunctionSpecTester::default().randn_size_cap"
    )]
    fn new(
        samples_per_batch_dims: usize,
        base_shapes_samples: usize,
        min_frac_successful: f64,
        min_frac_checked_batch: f64,
        start_num_inputs: usize,
        end_num_inputs: usize,
        start_ndim: usize,
        end_ndim: usize,
        start_shape_num: usize,
        end_shape_num: usize,
        test_with_rand: bool,
        randn_size_cap: usize,
    ) -> Self {
        Self {
            samples_per_batch_dims,
            base_shapes_samples,
            min_frac_successful,
            min_frac_checked_batch,
            start_num_inputs,
            end_num_inputs,
            start_ndim,
            end_ndim,
            start_shape_num,
            end_shape_num,
            test_with_rand,
            randn_size_cap,
        }
    }

    #[args(shapes_must_be_valid = "false")]
    pub fn test_from_shapes(
        &self,
        spec: GeneralFunctionSpec,
        shapes: Vec<Shape>,
        shapes_must_be_valid: bool,
    ) -> Result<(bool, bool)> {
        let GeneralFunctionShapeInfo {
            shape,
            num_non_batchable_output_dims,
            input_batchability,
        } = match spec.get_shape_info(&shapes) {
            Ok(info) => info,
            Err(e) => {
                if shapes_must_be_valid {
                    bail!(e.context("was supposed to be valid, but actually wasn't!"))
                }
                return Ok((false, false)); // No tests in case where this is invalid list of shapes
            }
        };

        if num_non_batchable_output_dims as usize > shape.len() {
            bail!(
            "too many non batchable output dims! num_non_batchable_output_dims={} shape.len()={}",
            num_non_batchable_output_dims,
            shape.len()
        );
        }
        if input_batchability.len() != shapes.len() {
            bail!(
                "input batchability len doesn't match! input_batchability.len()={} shapes.len()={}",
                input_batchability.len(),
                shapes.len()
            );
        }

        if input_batchability.iter().all(|x| !*x) {
            // if none batchable, we don't have any tests to run
            return Ok((true, false));
        }
        let current_num_batch_dims = shape.len() - num_non_batchable_output_dims as usize;

        for (shape, &is_batch) in
            std::iter::once((&shape, &true)).chain(shapes.iter().zip(&input_batchability))
        {
            if is_batch && shape.len() < current_num_batch_dims {
                bail!(
                "some batchable shape too short for batch, shape.len()={} current_num_batch_dims={}",
                shape.len(),
                current_num_batch_dims
            );
            }
        }

        let all_batch_shapes: HashSet<&[usize]> = std::iter::once(&shape[..current_num_batch_dims])
            .chain(
                shapes
                    .iter()
                    .zip(&input_batchability)
                    .filter_map(|(s, is_batch)| is_batch.then(|| &s[..current_num_batch_dims])),
            )
            .collect();
        if all_batch_shapes.len() != 1 {
            bail!(
                "inputs and output have non-matching 'batch' shapes, all_batch_shapes={:?}",
                all_batch_shapes
            );
        }

        let mut rng = rand::thread_rng();

        let mut run_sample = |num_batch_dims, random_inputs: bool| {
            let batch_shape: Shape = (0..num_batch_dims)
                .map(|_| rng.gen_range(self.start_shape_num..self.end_shape_num))
                .collect();

            let new_shapes: Vec<Shape> = shapes
                .iter()
                .zip(&input_batchability)
                .map(|(s, &is_batch)| {
                    if is_batch {
                        batch_shape
                            .iter()
                            .chain(&s[current_num_batch_dims..])
                            .cloned()
                            .collect()
                    } else {
                        s.clone()
                    }
                })
                .collect();

            let general_info = || {
                format!(
                    "shapes={:?} shape={:?} new_shapes={:?} current_num_batch_dims={}",
                    shapes, shape, new_shapes, current_num_batch_dims
                )
            };

            let new_info = spec.get_shape_info(&new_shapes).with_context(|| {
                format!(
                    "spec isn't consistent, error on valid shapes\n{}",
                    general_info()
                )
            })?;

            let prefix = "spec isn't consistent, ";

            if new_info.num_non_batchable_output_dims != num_non_batchable_output_dims {
                bail!(
                "{}changed num_non_batchable_output_dims when only batching was changed\n{}\n{}",
                prefix,
                format!(
                    "new_info.num_non_batchable_output_dims={} != num_non_batchable_output_dims={}",
                    new_info.num_non_batchable_output_dims, num_non_batchable_output_dims
                ),
                general_info()
            );
            }

            if &new_info.input_batchability != &input_batchability {
                bail!(
                    "{}changed input_batchability when only batching was changed\n{}\n{}",
                    prefix,
                    format!(
                        "new_info.input_batchability={:?} != input_batchability={:?}",
                        new_info.input_batchability, input_batchability
                    ),
                    general_info()
                );
            }

            let non_batch_shape = &shape[current_num_batch_dims..];
            let expected_shape = batch_shape
                .into_iter()
                .chain(non_batch_shape.iter().cloned())
                .collect::<Shape>();
            if new_info.shape != expected_shape {
                bail!(
                    "{}unexpected shape\n{}\n{}",
                    prefix,
                    format!(
                        "new_info.shape={:?} != expected_shape={:?}",
                        new_info.shape, expected_shape
                    ),
                    general_info()
                );
            }

            let get_count_find = |shapes: &[Shape], shape| {
                shapes
                    .iter()
                    .chain(std::iter::once(shape))
                    .map(|x| x.iter().product::<usize>())
                    .sum::<usize>()
                    < self.randn_size_cap
            };

            if random_inputs
                && get_count_find(&shapes, &shape)
                && get_count_find(&new_shapes, &new_info.shape)
                && num_batch_dims < current_num_batch_dims
            // only run random on < orig
            {
                // TODO: swap to f64 as needed!
                let tensors: Vec<_> = shapes
                    .iter()
                    .map(|shape| Array::randn(shape.clone()).value)
                    .collect();

                let out_tensor = spec
                    .function(&tensors, &TorchDeviceDtype::default())
                    .context("failed to evaluate for test")?;
                if out_tensor.shape() != &shape {
                    bail!(
                        "{}: unexpected tensor shape\n{}\n{}",
                        spec.name(),
                        format!(
                            "out_tensor.shape={:?} != shape={:?}",
                            out_tensor.shape(),
                            shape
                        ),
                        general_info()
                    );
                }
                let dims_to_remove = current_num_batch_dims - num_batch_dims;
                if shape[..dims_to_remove].iter().any(|x| *x == 0) {
                    return Ok(());
                }
                let idxs: Py<PyTuple> = Python::with_gil(|py| {
                    PyTuple::new(
                        py,
                        shape[..dims_to_remove]
                            .iter()
                            .map(|s| rng.gen_range(0..*s).into_py(py)),
                    )
                    .into()
                });
                let run_idx = |tensor: Tensor| tensor.py_getitem_acquire(idxs.clone()).unwrap();

                let new_tensor = spec
                    .function(
                        &tensors
                            .iter()
                            .zip(&input_batchability)
                            .map(|(x, &b)| if b { run_idx(x.clone()) } else { x.clone() })
                            .collect::<Vec<_>>(),
                        &Default::default(),
                    )
                    .context("failed to evaluate for test")?;

                let new_tensor_expected_shape: Shape =
                    shape[dims_to_remove..].iter().cloned().collect();
                if new_tensor.shape() != &new_tensor_expected_shape {
                    bail!(
                        "{}: unexpected tensor shape\n{}\n{}",
                        spec.name(),
                        format!(
                            "new_tensor.shape={:?} != expected_shape={:?}",
                            new_tensor.shape(),
                            expected_shape
                        ),
                        general_info()
                    );
                }

                assert_tensors_close(new_tensor, run_idx(out_tensor))
                    .context("tensors not close! (TODO: error)")?
            }

            Ok(())
        };

        for num_batch_dims in 0..current_num_batch_dims + 5 {
            for _ in 0..self.samples_per_batch_dims {
                run_sample(num_batch_dims, false)?;
            }
            run_sample(num_batch_dims, self.test_with_rand)?;
        }

        Ok((true, true))
    }

    pub fn test_many_shapes(&self, spec: GeneralFunctionSpec) -> Result<()> {
        let mut rng = rand::thread_rng();
        let mut any_frac_successful = false;
        let mut any_frac_checked_batch = false;
        let num_inputs_range = self.start_num_inputs..self.end_num_inputs;
        for num_inputs in num_inputs_range.clone() {
            let mut total_successful = 0.;
            let mut total_checked_batch = 0.;
            for _ in 0..self.base_shapes_samples {
                let shapes = (0..num_inputs)
                    .map(|_| {
                        let ndim = rng.gen_range(self.start_ndim..self.end_ndim);
                        (0..ndim)
                            .map(|_| rng.gen_range(self.start_shape_num..self.end_shape_num))
                            .collect()
                    })
                    .collect();

                let (was_successful, and_checked_batch) =
                    self.test_from_shapes(spec.clone(), shapes, false)?;
                total_successful += if was_successful { 1. } else { 0. };
                total_checked_batch += if and_checked_batch { 1. } else { 0. };
            }

            let frac_successful = total_successful / self.base_shapes_samples as f64;
            let frac_checked_batch = total_checked_batch / self.base_shapes_samples as f64;

            any_frac_successful =
                any_frac_successful || frac_successful >= self.min_frac_successful;
            any_frac_checked_batch =
                any_frac_checked_batch || frac_checked_batch >= self.min_frac_checked_batch;
        }

        if !num_inputs_range.is_empty() {
            if !any_frac_successful {
                bail!(
                    "frac successful too low\n{}\n{}",
                    "perhaps your function is too hard to automatically generate shapes for?",
                    "You can lower self.min_frac_successful to get this too pass, but you might not be testing very well"
                );
            }
            if !any_frac_checked_batch {
                bail!(
                    "frac check batch too low\n{}\n{}{}",
                    "perhaps your function is too hard to automatically generate batchable shapes for?",
                    "You can lower self.min_frac_checked_batch to get this too pass",
                    " (and you should set it to 0. if the function never supports batching)"
                );
            }
        }

        Ok(())
    }
}

#[test]
fn test_simple_general_function() -> Result<()> {
    pyo3::prepare_freethreaded_python();

    let tester = GeneralFunctionSpecTester {
        samples_per_batch_dims: 5,
        base_shapes_samples: 800,
        start_num_inputs: 0,
        end_num_inputs: 3,
        start_ndim: 0,
        end_ndim: 5,
        test_with_rand: false,
        ..Default::default()
    };

    for num_non_batchable_output_dims in 0..2 {
        for removed_from_end in 0..2 {
            let spec = GeneralFunctionSimpleSpec {
                name: "".to_owned(),
                num_non_batchable_output_dims,
                removed_from_end,
            }
            .into();
            tester.test_many_shapes(spec)?;
        }
    }
    // // TODO: this segfaults in pytorch and I can't seem to fix :/
    // // Note that tests work in python, so it must be something with
    // // prepare_freethreaded_python.
    // let tester_rand = GeneralFunctionSpecTester {
    //     test_with_rand: true,
    //     start_shape_num: 1,
    //     ..tester
    // };

    // for spec in SPECS.values() {
    //     tester_rand.test_many_shapes(spec.clone())?;
    // }

    Ok(())
}

#[test]
fn test_index_general_function() -> Result<()> {
    let tester = GeneralFunctionSpecTester {
        samples_per_batch_dims: 5,
        base_shapes_samples: 800,
        start_num_inputs: 1,
        end_num_inputs: 4,
        start_ndim: 0,
        end_ndim: 5,
        test_with_rand: false,
        ..Default::default()
    };

    let mut rng = rand::thread_rng();
    for index_dim in -2..2 {
        for batch_x in [false, true] {
            let spec = GeneralFunctionIndexSpec {
                index_dim,
                batch_x,
                check_index_ints: true,
            }
            .into();
            tester.test_many_shapes(spec)?;
        }

        let spec: GeneralFunctionSpec = GeneralFunctionIndexSpec {
            index_dim,
            batch_x: true,
            check_index_ints: true,
        }
        .into();
        for _ in 0..800 {
            let min_suffix_ndim = if index_dim < 0 {
                index_dim.abs()
            } else {
                index_dim + 1
            } as usize;
            let [prefix_shape, suffix_shape]: [Shape; 2] = [0, min_suffix_ndim]
                .into_iter()
                .map(|min_dims| {
                    let ndim = rng.gen_range(tester.start_ndim.max(min_dims)..tester.end_ndim);
                    (0..ndim)
                        .map(|_| rng.gen_range(tester.start_shape_num..tester.end_shape_num))
                        .collect()
                })
                .collect::<Vec<_>>()
                .try_into()
                .unwrap();
            assert!(suffix_shape.len() >= min_suffix_ndim);

            let x_shape: Shape = prefix_shape
                .iter()
                .cloned()
                .chain(suffix_shape.iter().cloned())
                .collect();
            let index_shape = prefix_shape.clone();

            tester
                .test_from_shapes(
                    spec.clone(),
                    vec![x_shape.clone(), index_shape.clone()],
                    true,
                )
                .with_context(|| {
                    format!(
                        "fail with x_shape={:?} index_shape={:?} suffix_shape={:?} index_dim={}",
                        x_shape, index_shape, suffix_shape, index_dim
                    )
                })?;
        }
    }

    Ok(())
}

fn convert_op_str_to_format_err(op_s: Option<&str>, path: &String) -> Result<String> {
    if let Some(s) = op_s {
        Ok(s.to_string())
    } else {
        Err(anyhow!(format!(
            "failed to parse general function from string: {}",
            path
        )))
    }
}

#[apply(python_error_exception)]
#[base_error_name(GeneralFunctionShape)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum GeneralFunctionShapeError {
    #[error("got={got} expected={expected} ({e_name})")]
    WrongNumShapes { got: usize, expected: usize },

    #[error("ndim={ndim} < num_non_batchable_output_dims={num_non_batchable_output_dims} + removed_from_end={removed_from_end} ({e_name})")]
    NDimTooSmall {
        ndim: usize,
        num_non_batchable_output_dims: u8,
        removed_from_end: u8,
    },

    #[error("x_shape={x_shape:?} index_shape={index_shape:?} batch_x={batch_x} ({e_name})")]
    IndexShapeInvalid {
        x_shape: Shape,
        index_shape: Shape,
        batch_x: bool,
    },
}
