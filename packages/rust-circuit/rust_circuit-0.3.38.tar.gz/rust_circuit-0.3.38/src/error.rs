use circuit_base::{
    expand_node::ExpandError,
    generalfunction::GeneralFunctionShapeError,
    module::SubstitutionError,
    named_axes::NamedAxesError,
    parsing::{ParseCircuitError, ReferenceCircError},
    ConstructError, TensorEvalError,
};
use circuit_rewrites::{
    algebraic_rewrite::{DistributeError, PushDownIndexError},
    batching::BatchError,
    deep_rewrite::SimpConfigError,
    scheduled_execution::{SchedulingError, SchedulingOOMError},
};
use get_update_node::{iterative_matcher::IterativeMatcherError, sampler::SampleError};
use nb_operations::{
    cumulant_rewrites::CumulantRewriteError,
    modules::{ExtractSymbolsError, ModuleBindError, PushDownModuleError},
    nest::NestError,
};
use pyo3::{types::PyModule, PyErr, PyResult, Python};
use rr_util::{
    errors_util::HasPythonException,
    rearrange_spec::{PermError, RearrangeParseError, RearrangeSpecError},
    symbolic_size::{SymbolicSizeOverflowError, SymbolicSizeSetError},
    tensor_util::{IndexError, MiscInputError, ParseError},
};
macro_rules! setup_errors {
    ($($t:ty),* $(,)?) => {
        pub fn anyhow_to_py_err(err: anyhow::Error) -> PyErr {
            $(
                if let Some(x) = err.root_cause().downcast_ref::<$t>() {
                    return x.get_py_err(format!("{:?}", err));
                }
            )*
            pyo3::anyhow::default_anyhow_to_py_err(err)
        }
        pub fn register_exceptions(py: Python<'_>, m: &PyModule) -> PyResult<()> {
            $(
                <$t>::register(py, m)?;
            )*
            Ok(())
        }
        pub fn print_exception_stubs(py : Python<'_>) -> PyResult<String> {
            let out = [
                $(
                    <$t>::print_stub(py)?,
                )*
            ].join("\n");
            Ok(out)
        }
    };
}

setup_errors!(
    BatchError,
    ConstructError,
    ExpandError,
    SubstitutionError,
    MiscInputError,
    ParseError,
    ParseCircuitError,
    RearrangeSpecError,
    PermError,
    RearrangeParseError,
    SchedulingError,
    SchedulingOOMError,
    TensorEvalError,
    SampleError,
    IndexError,
    NestError,
    PushDownIndexError,
    DistributeError,
    SimpConfigError,
    CumulantRewriteError,
    GeneralFunctionShapeError,
    ReferenceCircError,
    SymbolicSizeOverflowError,
    SymbolicSizeSetError,
    IterativeMatcherError,
    ModuleBindError,
    NamedAxesError,
    PushDownModuleError,
    ExtractSymbolsError
);
