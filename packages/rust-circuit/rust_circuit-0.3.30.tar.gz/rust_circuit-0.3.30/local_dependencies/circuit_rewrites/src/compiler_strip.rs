use circuit_base::{deep_map_op, deep_map_op_context, CircuitNode, CircuitRc};
use pyo3::prelude::*;

use crate::circuit_optimizer::OptimizationContext;

/// don't change symbols bc their names matter for correctness
#[pyfunction(disable_autoname = "false")]
#[pyo3(name = "strip_names")]
pub fn strip_names_py(circuit: CircuitRc, disable_autoname: bool) -> CircuitRc {
    strip_names(circuit, &mut Default::default(), disable_autoname)
}
pub fn strip_names(
    circuit: CircuitRc,
    context: &mut OptimizationContext,
    disable_autoname: bool,
) -> CircuitRc {
    deep_map_op_context(
        circuit.clone(),
        &|circuit, _| {
            (!circuit.is_irreducible_node()
                && (circuit.name().is_some()
                    || (disable_autoname && circuit.info().use_autoname())))
            .then(|| {
                let out = circuit.clone().rename(None);
                if disable_autoname {
                    // it's more logical to update the flag on irreducible_nodes, but
                    // then we get into issues with symbol equality which
                    // is annoying
                    out.with_autoname_disabled(true)
                } else {
                    out
                }
            })
        },
        &mut (),
        &mut context.cache.stripped_names,
    )
    .unwrap_or(circuit)
}

pub fn remove_autotags(circuit: CircuitRc) -> CircuitRc {
    deep_map_op(circuit.clone(), |c| {
        if let Some(at) = c.as_tag() {
            return Some(at.node.clone());
        }
        None
    })
    .unwrap_or(circuit)
}
