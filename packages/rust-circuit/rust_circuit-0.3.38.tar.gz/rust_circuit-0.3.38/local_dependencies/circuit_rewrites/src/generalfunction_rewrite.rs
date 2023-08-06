use circuit_base::{
    evaluate_device_dtype,
    generalfunction::{SpecTrait, OFFICIAL_GENERALFUNCTION_INVERSES},
    Circuit, CircuitNode, CircuitRc, GeneralFunction, Scalar,
};
use pyo3::prelude::*;
use rr_util::{
    sv,
    tensor_util::{TorchDeviceDtypeOp, TorchDtype},
};
#[pyfunction]
pub fn generalfunction_merge_inverses(circuit: &GeneralFunction) -> Option<CircuitRc> {
    if circuit.nodes.len()==1 && circuit.spec.is_official() && let Circuit::GeneralFunction(inner)=&**circuit.nodes[0] && inner.spec.is_official() && OFFICIAL_GENERALFUNCTION_INVERSES.iter().any(|(a,b)|*a==&circuit.spec.name()&&*b==&inner.spec.name()) {
        return Some(inner.nodes[0].clone())
    }
    None
}

#[pyfunction]
pub fn generalfunction_special_case_simplification(circuit: &GeneralFunction) -> Option<CircuitRc> {
    if circuit.spec.is_official() {
        let name_str: &str = &circuit.spec.name();
        match name_str {
            "softmax" => {
                if let Circuit::Scalar(_sc) = &**circuit.nodes[0] {
                    let scalar: f64 = 1.0
                        / circuit.nodes[0].info().shape[circuit.nodes[0].info().rank() - 1] as f64;
                    return Some(Scalar::nrc(
                        scalar,
                        circuit.info().shape.clone(),
                        circuit.name_cloned(),
                    ));
                }
            }
            "log_softmax" => {
                if let Circuit::Scalar(_sc) = &**circuit.nodes[0] {
                    let scalar: f64 = (1.0
                        / circuit.nodes[0].info().shape[circuit.nodes[0].info().rank() - 1] as f64)
                        .ln();
                    return Some(Scalar::nrc(
                        scalar,
                        circuit.info().shape.clone(),
                        circuit.name_cloned(),
                    ));
                }
            }
            _ => {}
        }
    }
    None
}

/// this does less than python version, maybe should expand
#[pyfunction]
pub fn generalfunction_evaluate_simple(node: &GeneralFunction) -> Option<CircuitRc> {
    if node.num_non_batchable_output_dims == 0
        && node.info().rank() == 0
        && node.nodes.len() == 1
        && node.nodes[0].info().rank() == 0
    {
        return node.nodes[0].as_scalar().map(|_inner| {
            Python::with_gil(|py| {
                Scalar::new(
                    evaluate_device_dtype(
                        node.crc(),
                        TorchDeviceDtypeOp {
                            device: None,
                            dtype: Some(TorchDtype::float64),
                        },
                    )
                    .unwrap()
                    .tensor()
                    .getattr(py, "item")
                    .unwrap()
                    .call(py, (), None)
                    .unwrap()
                    .extract(py)
                    .unwrap(),
                    sv![],
                    node.name_cloned(),
                )
                .rc()
            })
        });
    }
    None
}
