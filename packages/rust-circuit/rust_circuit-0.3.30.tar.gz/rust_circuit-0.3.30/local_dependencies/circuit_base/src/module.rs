use std::{
    hash::{Hash, Hasher},
    iter::{once, zip},
    // sync::{Arc, Weak},
};

use anyhow::{bail, Context, Result};
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, prelude::*, pyclass::CompareOp};
use rr_util::{
    cached_method,
    py_types::use_rust_comp,
    pycall, python_error_exception,
    rearrange_spec::RearrangeSpec,
    symbolic_size::SymbolicSizeProduct,
    tensor_util::{right_align_shapes, Shape, TorchDeviceDtype},
    util::{counts_g_1, is_unique},
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet, FxHasher};
use thiserror::Error;
use uuid::{uuid, Uuid};

use crate::{
    circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeHashItems, CircuitNodePrivate, CircuitNodeSetNonHashInfo},
    circuit_utils::OperatorPriority,
    deep_map, deep_map_op_context_preorder_stoppable, deep_map_preorder_unwrap, deep_map_unwrap,
    expand_node::{ExpandError, ReplaceExpander, ReplaceMapRc},
    named_axes::{deep_strip_axis_names, propagate_named_axes},
    new_rc_unwrap,
    prelude::*,
    visit_circuit_unwrap, CachedCircuitInfo, HashBytes, PyCircuitBase, Rearrange, Symbol,
    TensorEvalError,
};

/// can also be thought of as lambda from lambda calculus (expression with free variables + list of these variables)
#[pyclass]
#[derive(Debug, Clone, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct ModuleSpec {
    #[pyo3(get, set)]
    pub circuit: CircuitRc,
    #[pyo3(get, set)]
    pub arg_specs: Vec<ModuleArgSpec>,
}

type ModuleSpecHashable = (HashBytes, Vec<ModuleArgSpecHashable>);

pub fn are_args_used<'a, I: IntoIterator<Item = &'a ModuleArgSpec>>(
    circuit: &CircuitRc,
    arg_specs: I,
) -> Vec<bool>
where
    <I as IntoIterator>::IntoIter: DoubleEndedIterator,
{
    // right most binding has precedence, prior bindings unused
    let mut out: Vec<_> = arg_specs
        .into_iter()
        .rev()
        .scan(HashSet::default(), |prior_syms, spec| {
            let out = (!prior_syms.contains(&spec.symbol)) && has_free_sym(&circuit, &spec.symbol);
            prior_syms.insert(&spec.symbol);
            Some(out)
        })
        .collect();
    out.reverse();
    out
}

impl ModuleSpec {
    pub const EXPAND_PLACEHOLDER_UUID: Uuid = uuid!("741ba404-eec3-4ac9-b6ce-062e903fb033");

    pub fn get_hashable(&self) -> ModuleSpecHashable {
        (
            self.circuit.info().hash,
            self.arg_specs.iter().map(|x| x.get_hashable()).collect(),
        )
    }

    pub fn get_spec_circuit_uuid(&self) -> Uuid {
        let x: [_; 16] = self.circuit.info().hash[..16].try_into().unwrap();
        Uuid::from_bytes(x)
    }

    pub fn batch_shapes<'a>(&self, nodes: &'a [CircuitRc]) -> Vec<&'a [usize]> {
        zip(self.arg_specs.iter(), nodes)
            .map(|(arg_spec, node)| &node.shape()[..node.ndim() - arg_spec.symbol.ndim()])
            .collect()
    }

    pub fn aligned_batch_shape(&self, nodes: &[CircuitRc]) -> Result<Shape> {
        right_align_shapes(&self.batch_shapes(nodes))
    }

    pub fn expand_raw(&self, nodes: &Vec<CircuitRc>) -> Result<CircuitRc> {
        if self.arg_specs.len() != nodes.len() {
            bail!(ConstructError::ModuleWrongNumberChildren {
                expected: self.arg_specs.len(),
                got: nodes.len(),
                arg_specs: self.arg_specs.clone(),
                nodes: nodes.clone(),
            });
        }
        for (arg_spec, node) in zip(self.arg_specs.iter(), nodes) {
            if node.info().rank() < arg_spec.symbol.info().rank() {
                bail!(ExpandError::ModuleRankReduced {
                    node_rank: node.rank(),
                    symbol_rank: arg_spec.symbol.rank(),
                    arg_spec: arg_spec.clone(),
                    node_shape: node.shape().clone(),
                    spec_circuit: self.circuit.clone()
                });
            }
            if !arg_spec.batchable && node.info().rank() > arg_spec.symbol.info().rank() {
                bail!(ExpandError::ModuleTriedToBatchUnbatchableInput {
                    node_rank: node.rank(),
                    symbol_rank: arg_spec.symbol.rank(),
                    arg_spec: arg_spec.clone(),
                    spec_circuit: self.circuit.clone()
                });
            }
            if !arg_spec.expandable
                && node.info().shape[node.info().rank() - arg_spec.symbol.info().rank()..]
                    != arg_spec.symbol.info().shape[..]
            {
                bail!(ExpandError::ModuleTriedToExpandUnexpandableInput {
                    node_shape: node.shape().clone(),
                    symbol_shape: arg_spec.symbol.shape().clone(),
                    arg_spec: arg_spec.clone(),
                    spec_circuit: self.circuit.clone()
                });
            }
            if arg_spec.ban_non_symbolic_size_expand {
                for (dim, (&new_size, &old_size)) in node.shape()
                    [node.rank() - arg_spec.symbol.rank()..]
                    .iter()
                    .zip(arg_spec.symbol.shape())
                    .enumerate()
                {
                    if new_size != old_size && !SymbolicSizeProduct::has_symbolic(old_size) {
                        bail!(ExpandError::ModuleTriedToExpandOnNonSymbolicSizeAndBanned {
                            old_size,
                            new_size,
                            dim,
                            node_shape: node.shape().clone(),
                            arg_spec: arg_spec.clone(),
                            spec_circuit: self.circuit.clone()
                        });
                    }
                }
            }
        }

        // TODO: maybe we should allow for inconsistent symbolic batch shapes?
        let aligned_batch_shape = self
            .aligned_batch_shape(nodes)
            .context("batch shapes didn't match for module")?;

        // TODO: fix this being uncached!
        let out = ReplaceExpander::new_noop().replace_expand_with_map(
            self.circuit.clone(),
            &ReplaceMapRc::new(
                self.arg_specs
                    .iter()
                    .zip(nodes)
                    .map(|(arg_spec, node)| (arg_spec.symbol.crc(), node.clone()))
                    .collect(),
            ),
        )?;

        assert!(out.ndim() >= self.circuit.ndim());
        let out_batch_rank = out.ndim() - self.circuit.ndim();
        assert!(out_batch_rank <= aligned_batch_shape.len());
        right_align_shapes(&[&out.shape()[..out_batch_rank], &aligned_batch_shape])
            .expect("output shape should be right aligned subset of batch shape");

        let out = if out_batch_rank < aligned_batch_shape.len() {
            let extra_batch = aligned_batch_shape.len() - out_batch_rank;
            let spec = RearrangeSpec::prepend_batch_shape(
                aligned_batch_shape[..extra_batch].iter().cloned().collect(),
                out.ndim(),
            )
            .context("rank overflow in module expand")?;

            let rep_name = out.name().map(|x| format!("{} rep_batch", x));
            Rearrange::nrc(out, spec, rep_name)
        } else {
            out
        };
        Ok(out)
    }

    pub fn expand_shape(&self, shapes: &Vec<Shape>) -> Result<(CircuitRc, Vec<HashBytes>)> {
        let key = (self.get_hashable(), shapes.clone());
        if let Some(result) = MODULE_EXPANSIONS_SHAPE.with(|cache| {
            let borrowed = cache.borrow();
            if let Some((w, shapes)) = borrowed.get(&key) {
                return Some((w.clone(), shapes.clone()));

                // if let Some(w) = w.upgrade() {
                //     return Some((CircuitRc(w), shapes.clone()));
                // } else {
                //     drop(borrowed);
                //     cache.borrow_mut().remove(&key);
                // }
            }
            None
        }) {
            return Ok(result);
        }
        let symbols = shapes
            .iter()
            .enumerate()
            .map(|(i, s)| {
                Symbol::nrc(
                    s.clone(),
                    self.get_spec_circuit_uuid(),
                    Some(format!("{}_{:?}", i, s)),
                )
            })
            .collect();
        let result = self.expand_raw(&symbols)?;
        let out_bytes: Vec<_> = symbols.into_iter().map(|x| x.info().hash).collect();
        MODULE_EXPANSIONS_SHAPE.with(|cache| {
            cache.borrow_mut().insert(
                (self.get_hashable(), shapes.clone()),
                (
                    // Arc::downgrade(&result.0)
                    result.clone(),
                    out_bytes.clone(),
                ),
            )
        });
        Ok((result, out_bytes))
    }

    pub fn substitute(
        &self,
        nodes: &Vec<CircuitRc>,
        name_prefix: Option<String>,
        name_suffix: Option<String>,
    ) -> Result<CircuitRc> {
        let key: (_, Vec<HashBytes>, Option<String>) = (
            self.get_hashable(),
            nodes.iter().map(|x| x.info().hash).collect(),
            name_prefix.clone(),
        );

        if let Some(result) = MODULE_EXPANSIONS.with(|cache| {
            let borrowed = cache.borrow();
            if let Some(w) = borrowed.get(&key) {
                return Some(w.clone());
                // if let Some(w) = w.upgrade() {
                //     return Some(CircuitRc(w));
                // } else {
                //     drop(borrowed);
                //     cache.borrow_mut().remove(&key);
                // }
            }
            None
        }) {
            return Ok(result);
        }

        for (arg_spec, sub_for_sym) in self.arg_specs.iter().zip(nodes) {
            check_valid_sub(&self.circuit, &arg_spec.symbol, sub_for_sym)?
        }

        let shapes = nodes.iter().map(|x| x.info().shape.clone()).collect();
        let (mut expanded_shape, rep_hashes) = self.expand_shape(&shapes)?;
        let node_mapping: HashMap<_, _> = rep_hashes.into_iter().zip(nodes).collect();
        if name_prefix.is_some() || name_suffix.is_some() {
            expanded_shape = deep_map_unwrap(expanded_shape, |x| {
                if let Some(n) = x.name() {
                    if !node_mapping.contains_key(&x.info().hash) {
                        return x.clone().rename(Some(
                            name_prefix.clone().unwrap_or_else(|| "".to_owned())
                                + n
                                + name_suffix.as_ref().map(|x| -> &str { x }).unwrap_or(""),
                        ));
                    }
                }
                x.clone()
            })
        }
        // we're replacing leaves so no need to do anything with stoppable preorder
        let result = deep_map(expanded_shape, |circ| {
            Ok(node_mapping
                .get(&circ.info().hash)
                .cloned()
                .cloned()
                .unwrap_or(circ))
        })
        .with_context(|| {
            format!(
                concat!(
                    "replacing symbols with nodes",
                    " failed in ModuleSpec substitute\n",
                    "This is typically caused by multiple dtypes ",
                    "(see root cause below)\n",
                    "module_spec={:?}\nnodes={:?}"
                ),
                self, nodes
            )
        })?;
        MODULE_EXPANSIONS.with(|cache| {
            cache.borrow_mut().insert(
                key,
                result.clone(), // Arc::downgrade(&result.0)
            )
        });
        Ok(result)
    }

    pub fn compute_non_children_hash(&self, hasher: &mut blake3::Hasher) {
        for arg_spec in &self.arg_specs {
            // this is fine because each item is fixed size and we delimit with node hashs (which are uu)
            hasher.update(&[
                arg_spec.batchable as u8,
                arg_spec.expandable as u8,
                arg_spec.ban_non_symbolic_size_expand as u8,
            ]);
            hasher.update(&arg_spec.symbol.info().hash);
        }
    }

    pub fn map_circuit<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(CircuitRc) -> Result<CircuitRc>,
    {
        Ok(ModuleSpec {
            circuit: f(self.circuit.clone())?,
            arg_specs: self.arg_specs.clone(),
        })
    }
    pub fn map_circuit_unwrap<F>(&self, mut f: F) -> Self
    where
        F: FnMut(CircuitRc) -> CircuitRc,
    {
        ModuleSpec {
            circuit: f(self.circuit.clone()),
            arg_specs: self.arg_specs.clone(),
        }
    }
}

#[pyfunction]
pub fn all_free(circuit: CircuitRc) -> Vec<Symbol> {
    // returns syms in circuit visit order (order maybe matters here)
    let mut all_syms = Vec::new();
    visit_circuit_unwrap(substitute_all_modules(circuit), |x| {
        if let Some(sym) = x.as_symbol() {
            all_syms.push(sym.clone())
        }
    });
    all_syms
}

#[pymethods]
impl ModuleSpec {
    #[new]
    #[args(check_all_inputs_used = "true", check_unique_arg_names = "true")]
    pub fn new(
        circuit: CircuitRc,
        arg_specs: Vec<ModuleArgSpec>,
        check_all_inputs_used: bool,
        check_unique_arg_names: bool,
    ) -> Result<Self> {
        let out = Self { circuit, arg_specs };
        if check_all_inputs_used {
            out.check_all_inputs_used()?;
        }
        if check_unique_arg_names {
            out.check_unique_arg_names()?;
        }
        Ok(out)
    }

    pub fn check_all_inputs_used(&self) -> Result<()> {
        let missing_symbols: HashSet<_> = self
            .are_args_used()
            .into_iter()
            .zip(&self.arg_specs)
            .filter_map(|(used, arg_spec)| (!used).then(|| arg_spec.symbol.clone()))
            .collect();
        if !missing_symbols.is_empty() {
            bail!(ConstructError::ModuleSomeArgsNotPresent {
                spec_circuit: self.circuit.clone(),
                missing_symbols,
            })
        }
        Ok(())
    }

    pub fn check_unique_arg_names(&self) -> Result<()> {
        // TODO: maybe cache me (as needed)!
        if self.arg_specs.iter().any(|x| x.symbol.name().is_none()) {
            bail!(ConstructError::ModuleSomeArgsNamedNone {
                symbols_named_none: self
                    .arg_specs
                    .iter()
                    .filter_map(|x| x.symbol.name().is_none().then(|| x.symbol.clone()))
                    .collect()
            })
        }
        let names: Vec<_> = self
            .arg_specs
            .iter()
            .map(|x| x.symbol.name().unwrap())
            .collect();
        if !is_unique(&names) {
            bail!(ConstructError::ModuleArgsDupNames {
                dup_names: counts_g_1(names.into_iter().map(|x| x.to_owned()))
            })
        }

        Ok(())
    }

    #[pyo3(name = "map_circuit")]
    pub fn map_circuit_py(&self, f: PyObject) -> Result<Self> {
        self.map_circuit(|x| pycall!(f, (x,), anyhow))
    }

    #[staticmethod]
    #[args(check_unique_arg_names = "true")]
    pub fn new_all_free(circuit: CircuitRc, check_unique_arg_names: bool) -> Result<Self> {
        let arg_specs = all_free(circuit.clone())
            .into_iter()
            .map(|x| ModuleArgSpec::new(x, true, true, true))
            .collect();
        let out =
            Self::new(circuit, arg_specs, true, false).expect("method should guarantee valid");
        if check_unique_arg_names {
            // check after instead of in new so we can .expect on other errors in new
            out.check_unique_arg_names()?;
        }
        // maybe we should use no_check_args for speed
        Ok(out)
    }

    #[staticmethod]
    #[args(check_all_inputs_used = "true", check_unique_arg_names = "true")]
    pub fn new_extract(
        circuit: CircuitRc,
        arg_specs: Vec<(CircuitRc, ModuleArgSpec)>,
        check_all_inputs_used: bool,
        check_unique_arg_names: bool,
    ) -> Result<Self> {
        let mut new_arg_specs: Vec<Option<ModuleArgSpec>> = vec![None; arg_specs.len()];
        let spec_circuit = deep_map_op_context_preorder_stoppable(
            circuit.clone(),
            &|circuit,
              c: &mut (
                &mut Vec<Option<ModuleArgSpec>>,
                &Vec<(CircuitRc, ModuleArgSpec)>,
            )| {
                let (real_arg_specs, proposed_arg_specs) = c;
                if let Some(i) = proposed_arg_specs
                    .iter()
                    .position(|x| x.0.info().hash == circuit.info().hash)
                {
                    let mut arg_spec = proposed_arg_specs[i].1.clone();
                    arg_spec.symbol = Symbol::new(
                        circuit.info().shape.clone(),
                        arg_spec.symbol.uuid,
                        arg_spec.symbol.name_cloned().or(circuit.name_cloned()),
                    );
                    real_arg_specs[i] = Some(arg_spec);
                    return (Some(real_arg_specs[i].as_ref().unwrap().symbol.crc()), true);
                }
                (None, false)
            },
            &mut (&mut new_arg_specs, &arg_specs),
            &mut Default::default(),
        )
        .unwrap_or(circuit);
        let new_arg_specs: Vec<ModuleArgSpec> = if check_all_inputs_used {
            let er = new_arg_specs
                .iter()
                .cloned()
                .collect::<Option<Vec<_>>>()
                .ok_or_else(|| ConstructError::ModuleExtractNotPresent {
                    subcirc: arg_specs[new_arg_specs.iter().position(|x| x.is_none()).unwrap()]
                        .0
                        .clone(),
                });
            er?
        } else {
            new_arg_specs
                .into_iter()
                // TODO: maybe instead of filter we're supposed to just have missing module args?
                .filter(|z| z.is_some())
                .collect::<Option<Vec<_>>>()
                .unwrap()
        };
        // maybe we should use no_check_args for speed
        let out = Self::new(spec_circuit, new_arg_specs, check_all_inputs_used, false)
            .expect("method should guarantee valid");
        if check_unique_arg_names {
            // check after instead of in new so we can .expect on other errors in new
            out.check_unique_arg_names()?;
        }
        Ok(out)
    }

    // TODO: add some naming options maybe
    pub fn resize(&self, shapes: Vec<Shape>) -> Result<Self> {
        let arg_specs: Vec<ModuleArgSpec> = zip(&self.arg_specs, shapes)
            .map(|(arg_spec, shape)| ModuleArgSpec {
                symbol: Symbol::new(shape, arg_spec.symbol.uuid, arg_spec.symbol.name_cloned()),
                ..arg_spec.clone()
            })
            .collect();

        let circuit = self
            .substitute(
                &arg_specs.iter().map(|x| x.symbol.crc()).collect(),
                None,
                None,
            )
            .context("substitute failed from resize")?;
        Ok(Self { circuit, arg_specs })
    }

    pub fn are_args_used(&self) -> Vec<bool> {
        are_args_used(&self.circuit, &self.arg_specs)
    }

    pub fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self, &object, comp_op)
    }

    fn __hash__(&self) -> u64 {
        let mut s = FxHasher::default();
        self.hash(&mut s);
        s.finish()
    }
}

#[pyclass]
#[derive(Debug, Clone, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct ModuleArgSpec {
    #[pyo3(get, set)]
    pub symbol: Symbol,
    #[pyo3(get, set)]
    pub batchable: bool,
    #[pyo3(get, set)]
    pub expandable: bool,
    #[pyo3(get, set)]
    pub ban_non_symbolic_size_expand: bool,
}

impl Default for ModuleArgSpec {
    fn default() -> Self {
        Self {
            symbol: Symbol::new_with_none_uuid([].into_iter().collect(), None),
            batchable: true,
            expandable: true,
            ban_non_symbolic_size_expand: true,
        }
    }
}

pub type ModuleArgSpecHashable = (HashBytes, [bool; 3]);

impl ModuleArgSpec {
    pub fn get_hashable(&self) -> ModuleArgSpecHashable {
        (
            self.symbol.info().hash,
            [
                self.batchable,
                self.expandable,
                self.ban_non_symbolic_size_expand,
            ],
        )
    }
}

#[pymethods]
impl ModuleArgSpec {
    #[new]
    #[args(
        batchable = "Self::default().batchable",
        expandable = "Self::default().expandable",
        ban_non_symbolic_size_expand = "Self::default().ban_non_symbolic_size_expand"
    )]
    fn new(
        symbol: Symbol,
        batchable: bool,
        expandable: bool,
        ban_non_symbolic_size_expand: bool,
    ) -> Self {
        Self {
            symbol,
            batchable,
            expandable,
            ban_non_symbolic_size_expand,
        }
    }
    #[staticmethod]
    #[args(
        batchable = "Self::default().batchable",
        expandable = "Self::default().expandable",
        ban_non_symbolic_size_expand = "false", // I think this is right default for this?
    )]
    pub fn just_name_shape(
        circuit: CircuitRc,
        batchable: bool,
        expandable: bool,
        ban_non_symbolic_size_expand: bool,
    ) -> Self {
        Self {
            symbol: Symbol::new_with_random_uuid(
                circuit.info().shape.clone(),
                circuit.name_cloned(),
            ),
            batchable,
            expandable,
            ban_non_symbolic_size_expand,
        }
    }

    pub fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self, &object, comp_op)
    }

    fn __hash__(&self) -> u64 {
        let mut s = FxHasher::default();
        self.hash(&mut s);
        s.finish()
    }
}

/// can also be thought of as a lambda + it's arguments in lambda calculus (but not yet beta reduced)
/// aka call site
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Module {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    #[pyo3(get)]
    pub spec: ModuleSpec,
    cached_substituted: CircuitRc,
    info: CachedCircuitInfo,
    #[pyo3(get)]
    name: Option<String>,
}

impl Module {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, spec: ModuleSpec, name: Option<String>) -> Result<Self> {
        let cached_substituted = spec
            .substitute(&nodes, None, None)
            .with_context(|| format!("module construction failed on substitute name={:?}", name))?;

        let out = Self {
            nodes,
            spec,
            cached_substituted,
            name,
            info: Default::default(),
        };
        out.initial_init_info()
    }

    pub fn new_kwargs(
        kwargs: &HashMap<String, CircuitRc>,
        spec: ModuleSpec,
        name: Option<String>,
    ) -> Result<Self> {
        let mut nodes: Vec<_> = vec![None; spec.arg_specs.len()];
        spec.check_unique_arg_names()?;
        for (k, v) in kwargs {
            match spec
                .arg_specs
                .iter()
                .position(|x| x.symbol.name().expect("check_unique_arg_names above") == k)
            {
                Some(i) => {
                    nodes[i] = Some(v.clone());
                }
                None => {
                    bail!(ConstructError::ModuleUnknownArgument {
                        argument: k.clone(),
                        all_module_inputs: spec
                            .arg_specs
                            .iter()
                            .map(|x| x.symbol.name_cloned().unwrap())
                            .collect()
                    })
                }
            }
        }
        if nodes.iter().any(|x| x.is_none()) {
            bail!(ConstructError::ModuleMissingNames {
                missing_arguments: nodes
                    .iter()
                    .zip(spec.arg_specs)
                    .filter_map(|(n, arg_spec)| n.is_none().then(|| arg_spec
                        .symbol
                        .name_cloned()
                        .expect("check_unique_arg_names above")))
                    .collect()
            });
        }

        Self::try_new(nodes.into_iter().map(Option::unwrap).collect(), spec, name)
    }

    fn child_axis_map_inputs_uncached(&self) -> Result<Vec<Vec<Option<usize>>>> {
        let spec_resized = self
            .spec
            .resize(self.nodes.iter().map(|x| x.info().shape.clone()).collect())?;
        let spec_circuit_resized = spec_resized.circuit.clone();
        assert!(spec_circuit_resized.info().shape[..] == self.info().shape[..]);
        let stripped = deep_strip_axis_names(spec_circuit_resized, &None);
        let out_named = propagate_named_axes(
            stripped,
            (0..self.info().rank())
                .map(|i| (i as u8, i.to_string()))
                .collect(),
            true,
        );
        let mut result: Vec<Vec<Option<usize>>> = self
            .nodes
            .iter()
            .map(|c| vec![None; c.info().rank()])
            .collect();
        visit_circuit_unwrap(out_named, |x| {
            if let Some(sym) = x.as_symbol() {
                if let Some(i) = self
                    .spec
                    .arg_specs
                    .iter()
                    .position(|x| x.symbol.uuid == sym.uuid && x.symbol.name() == sym.name())
                {
                    for (k, v) in &sym.info().named_axes {
                        result[i][*k as usize] = Some(v.parse::<usize>().unwrap());
                    }
                }
            }
        });
        Ok(result)
    }
}

circuit_node_extra_impl!(Module, self_hash_default);

impl CircuitNodeHashItems for Module {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        self.spec.compute_non_children_hash(hasher)
    }
}

impl CircuitNodeSetNonHashInfo for Module {
    fn set_non_hash_info(&mut self) -> Result<()> {
        *self.info_mut() = self.cached_substituted.info().clone();
        Ok(())
    }
}

impl CircuitNode for Module {
    circuit_node_auto_impl!("6825f723-f178-4dab-b568-cd85eb6d2bf3");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let map_inputs = self.child_axis_map_inputs().unwrap();
        once(vec![None; self.spec.circuit.info().rank()])
            .chain(map_inputs)
            .collect()
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(std::iter::once(self.spec.circuit.clone()).chain(self.nodes.clone()))
    }

    fn non_free_children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        let new_spec_circ = f(0, self.spec.circuit.clone())?;

        assert_eq!(
            self.spec.arg_specs.len(),
            self.nodes.len(),
            "guaranteed by constructor via expand"
        );

        let nodes = self
            .nodes
            .clone()
            .into_iter()
            .enumerate()
            .map(|(i, node)| f(i + 1, node))
            .collect::<Result<_>>()?;

        Self::try_new(
            nodes,
            ModuleSpec {
                circuit: new_spec_circ,
                arg_specs: self.spec.arg_specs.clone(),
            },
            self.name.clone(),
        )
    }

    fn map_non_free_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        let nodes = self
            .nodes
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, x)| f(i, x))
            .collect::<Result<_>>()?;
        Self::try_new(nodes, self.spec.clone(), self.name_cloned())
    }

    fn eval_tensors(
        &self,
        _tensors: &[rr_util::py_types::Tensor],
        _device_dtype: &TorchDeviceDtype,
    ) -> Result<rr_util::py_types::Tensor> {
        bail!(TensorEvalError::ModulesCantBeDirectlyEvalutedInternal {
            module: self.clone(),
        })
    }
}

impl CircuitNodeAutoName for Module {
    const PRIORITY: OperatorPriority = OperatorPriority::Function {};

    fn auto_name(&self) -> Option<String> {
        if self.children().any(|x| x.name().is_none()) {
            None
        } else {
            Some(
                self.spec.circuit.name_cloned().unwrap()
                    + "("
                    + &self
                        .nodes
                        .iter()
                        .map(|node| node.name_cloned().unwrap())
                        .collect::<Vec<String>>()
                        .join(", ")
                    + ")",
            )
        }
    }
}

#[pymethods]
impl Module {
    #[new]
    #[args(name = "None", kwargs = "**")]
    fn new_py(
        spec: ModuleSpec,
        name: Option<String>,
        kwargs: Option<HashMap<String, CircuitRc>>,
    ) -> PyResult<PyClassInitializer<Module>> {
        Ok(Module::new_kwargs(&kwargs.unwrap_or_else(HashMap::default), spec, name)?.into_init())
    }

    #[staticmethod]
    #[args(nodes = "*", name = "None")]
    fn new_flat(spec: ModuleSpec, nodes: Vec<CircuitRc>, name: Option<String>) -> Result<Self> {
        Self::try_new(nodes, spec, name)
    }

    /// TODO: fancier renaming technology?
    #[pyo3(name = "substitute")]
    #[args(
        name_prefix = "None",
        name_suffix = "None",
        use_self_name_as_prefix = "false"
    )]
    pub fn substitute_py(
        &self,
        name_prefix: Option<String>,
        name_suffix: Option<String>,
        use_self_name_as_prefix: bool,
    ) -> Result<CircuitRc> {
        let name_prefix = if use_self_name_as_prefix {
            if let Some(name_prefix) = name_prefix {
                bail!(
                    ConstructError::ModulePassedNamePrefixAndUseSelfNameAsPrefix {
                        name_prefix,
                        module: self.clone()
                    }
                )
            }

            self.name_cloned().map(|x| x + ".")
        } else {
            name_prefix
        };
        Ok(self.substitute(name_prefix, name_suffix))
    }

    pub fn aligned_batch_shape(&self) -> Shape {
        self.spec.aligned_batch_shape(&self.nodes).unwrap()
    }

    /// None is conform all dims
    pub fn conform_to_input_batch_shape(&self, dims_to_conform: Option<usize>) -> Result<Self> {
        let current_aligned = self.aligned_batch_shape();
        let dims_to_conform = dims_to_conform.unwrap_or(current_aligned.len());

        if dims_to_conform > current_aligned.len() {
            // better error as needed
            bail!("dims to conform is larger than num batch dims!")
        }

        let batch_shapes = self.spec.batch_shapes(&self.nodes);

        Ok(Self::new(
            self.nodes.clone(),
            self.spec
                .resize(
                    self.spec
                        .arg_specs
                        .iter()
                        .zip(&batch_shapes)
                        .map(|(arg_spec, current_batch_shape)| {
                            let batch_start =
                                current_batch_shape.len().saturating_sub(dims_to_conform);
                            current_batch_shape[batch_start..]
                                .iter()
                                .chain(arg_spec.symbol.shape())
                                .copied()
                                .collect()
                        })
                        .collect(),
                )
                .expect("constructor should ensure this works"),
            self.name_cloned(),
        ))
    }

    // TODO: add some naming options maybe
    pub fn conform_to_input_shapes(&self) -> Self {
        Self::new(
            self.nodes.clone(),
            self.spec
                .resize(self.nodes.iter().map(|x| x.shape().clone()).collect())
                .expect("constructor should ensure this works"),
            self.name_cloned(),
        )
    }

    fn child_axis_map_inputs(&self) -> Result<Vec<Vec<Option<usize>>>> {
        let key = (
            self.spec.get_hashable(),
            self.nodes.iter().map(|x| x.info().shape.clone()).collect(),
        );
        if let Some(result) =
            MODULE_EXPANSIONS_AXIS_MAPS.with(|cache| cache.borrow().get(&key).cloned())
        {
            return Ok(result);
        }

        let result = self.child_axis_map_inputs_uncached()?;
        MODULE_EXPANSIONS_AXIS_MAPS.with(|cache| cache.borrow_mut().insert(key, result.clone()));
        Ok(result)
    }

    pub fn arg_items(&self) -> Vec<(CircuitRc, ModuleArgSpec)> {
        self.nodes
            .clone()
            .into_iter()
            .zip(self.spec.arg_specs.clone())
            .collect()
    }
}

impl Module {
    pub fn substitute_self_name_prefix(&self) -> CircuitRc {
        self.substitute(self.name_cloned().map(|x| x + "."), None)
    }

    pub fn substitute(
        &self,
        name_prefix: Option<String>,
        name_suffix: Option<String>,
    ) -> CircuitRc {
        self.spec
            .substitute(&self.nodes, name_prefix, name_suffix)
            .map(|x| x.rename(self.name_cloned()))
            .expect("constructor should ensure this works")
    }
}

#[pyfunction]
pub fn substitute_all_modules(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(circuit, |c| match &**c {
        Circuit::Module(mn) => mn.substitute(None, None),
        _ => c.clone(),
    })
}

#[pyfunction]
pub fn conform_all_modules(circuit: CircuitRc) -> CircuitRc {
    // this has to be preorder so that we resolve to outermost sizes
    deep_map_preorder_unwrap(circuit, |c| match &**c {
        Circuit::Module(mn) => mn.conform_to_input_shapes().rc(),
        _ => c.clone(),
    })
}

#[pyfunction]
pub fn get_children_with_symbolic_sizes(circuit: CircuitRc) -> HashSet<CircuitRc> {
    let mut circuits_with_symbolic_sizes = HashSet::default();
    visit_circuit_unwrap(circuit, |x| {
        if x.shape()
            .iter()
            .any(|s| SymbolicSizeProduct::has_symbolic(*s))
        {
            circuits_with_symbolic_sizes.insert(x);
        }
    });
    circuits_with_symbolic_sizes
}

#[pyfunction]
pub fn any_children_with_symbolic_sizes(circuit: CircuitRc) -> bool {
    !get_children_with_symbolic_sizes(circuit).is_empty()
}

// adhoc anyfound
// TODO: do this batchedly over symbols while still caching individually?
#[derive(Clone, Debug)]
pub struct HasFreeSym {
    cache: cached::UnboundCache<(HashBytes, HashBytes), bool>,
}
impl Default for HasFreeSym {
    fn default() -> Self {
        Self {
            cache: cached::UnboundCache::new(),
        }
    }
}
impl HasFreeSym {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, sym.info().hash))]
    #[cache_expr(cache)]
    pub fn has_free_sym(&mut self, circuit: &CircuitRc, sym: &Symbol) -> bool {
        if circuit.as_symbol() == Some(sym) {
            return true;
        }

        if let Some(m) = circuit.as_module() {
            if m.spec
                .arg_specs
                .iter()
                .any(|arg_spec| &arg_spec.symbol == sym)
            {
                // skip spec circuit if bound
                return m.nodes.iter().any(|c| self_.has_free_sym(&c, sym));
            }
        }

        circuit.children().any(|c| self_.has_free_sym(&c, sym))
    }
}

/// uses global cache
pub fn has_free_sym(circuit: &CircuitRc, sym: &Symbol) -> bool {
    HAS_FREE_SYM.with(|has_free_sym| has_free_sym.borrow_mut().has_free_sym(circuit, sym))
}

// adhoc anyfound
// TODO: do this batchedly over symbols while still caching individually?
#[derive(Clone, Debug)]
pub struct CheckValidSub {
    cache: cached::UnboundCache<(HashBytes, HashBytes, HashBytes), ()>,
}
impl Default for CheckValidSub {
    fn default() -> Self {
        Self {
            cache: cached::UnboundCache::new(),
        }
    }
}
impl CheckValidSub {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, sym.info().hash, sub_for_sym.info().hash))]
    #[use_try]
    #[cache_expr(cache)]
    pub fn check_valid_sub(
        &mut self,
        circuit: &CircuitRc,
        sym: &Symbol,
        sub_for_sym: &CircuitRc,
    ) -> Result<()> {
        if let Some(sym_here) = circuit.as_symbol() {
            if sym_here != sym && sym_here.ident() == sym.ident() {
                bail!(
                    SubstitutionError::FoundNEQFreeSymbolWithSameIdentification {
                        sym: sym.clone(),
                        matching_sym: sym_here.clone()
                    }
                )
            }
        }

        circuit
            .non_free_children() // do this first so we error at inner most module!
            .map(|c| self_.check_valid_sub(&c, sym, sub_for_sym))
            .collect::<Result<()>>()?;

        if let Some(m) = circuit.as_module() {
            if m.spec
                .arg_specs
                .iter()
                .any(|arg_spec| &arg_spec.symbol == sym)
            {
                // skip spec circuit if bound
                return m
                    .nodes
                    .iter()
                    .map(|c| self_.check_valid_sub(&c, sym, sub_for_sym))
                    .collect();
            }
            // otherwise, we might sub into the spec circuit
            if has_free_sym(&m.spec.circuit, sym) {
                let used_args = are_args_used(sub_for_sym, &m.spec.arg_specs);

                if used_args.iter().any(|x| *x) {
                    bail!(SubstitutionError::CircuitHasFreeSymsBoundByNestedModule {
                        circ: sub_for_sym.clone(),
                        sym: sym.clone(),
                        nested_module: m.clone(),
                        bound_by_nested: m
                            .spec
                            .arg_specs
                            .iter()
                            .zip(used_args)
                            .filter_map(|(arg_spec, used)| used.then(|| arg_spec.symbol.clone()))
                            .collect()
                    })
                }
            }
        }

        Ok(())
    }
}

pub fn check_valid_sub(circuit: &CircuitRc, sym: &Symbol, sub_for_sym: &CircuitRc) -> Result<()> {
    CHECK_VALID_SUB.with(|check_valid_sub| {
        check_valid_sub
            .borrow_mut()
            .check_valid_sub(circuit, sym, sub_for_sym)
    })
}

const SAME_IDENT_P1 :&str = "Substituting for a symbol when there is a not-equal free symbol with the same name and uuid is not allowed (aka, a near miss).";
const SAME_IDENT_P2: &str = "This is caused by having a different shape (or different named axes).";

#[apply(python_error_exception)]
#[base_error_name(Substitution)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum SubstitutionError {
    #[error("subbing circ={circ:?} for sym={sym:?} results in nested_module={nested_module:?} bound_by_nested={bound_by_nested:?} {} ({e_name})",
        "inside of circ (aka higher order function)")]
    CircuitHasFreeSymsBoundByNestedModule {
        circ: CircuitRc,
        sym: Symbol,
        nested_module: Module,
        bound_by_nested: Vec<Symbol>,
    },

    #[error(
        "sym={sym:?} matching_sym={matching_sym:?}\n{SAME_IDENT_P1}\n{SAME_IDENT_P2}\n({e_name})"
    )]
    FoundNEQFreeSymbolWithSameIdentification { sym: Symbol, matching_sym: Symbol },
}

use std::cell::RefCell;
// TODO: maybe cache check_unique_arg_names here?
// TODO: avoid caching arrays forever!
// TODO: make modules much faster by avoiding exponential time blow up!
thread_local! {
    static MODULE_EXPANSIONS: RefCell<
        HashMap<
            (ModuleSpecHashable, Vec<HashBytes>, Option<String>),
            CircuitRc, // Weak<Circuit>
        >,
    > = RefCell::new(HashMap::default());
    static MODULE_EXPANSIONS_SHAPE: RefCell<
        HashMap<
            (ModuleSpecHashable, Vec<Shape>),
            (
                CircuitRc, // Weak<Circuit>
                Vec<HashBytes>,
            ),
        >,
    > = RefCell::new(HashMap::default());
    static MODULE_EXPANSIONS_AXIS_MAPS: RefCell<
        HashMap<(ModuleSpecHashable, Vec<Shape>), Vec<Vec<Option<usize>>>>,
    > = RefCell::new(HashMap::default());
    static CHECK_VALID_SUB: RefCell<CheckValidSub> = RefCell::new(Default::default());
    static HAS_FREE_SYM: RefCell<HasFreeSym> = RefCell::new(Default::default());
}
