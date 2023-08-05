use std::{
    fmt::Write,
    iter::{once, zip},
};

use anyhow::Result;
use circuit_base::{
    clicolor,
    print::{color, CliColor, PrintOptions},
    CircuitNode, CircuitNodeSelfOnlyHash, CircuitRc,
};
use itertools::Itertools;
use once_cell::unsync::Lazy;
use pyo3::prelude::*;
use rr_util::util::{indent, HashBytes};
use rustc_hash::FxHashMap as HashMap;
use uuid::uuid;
#[pyfunction(
    hash_child_count = "true",
    hash_child_shapes = "false",
    hash_name = "true"
)]
pub fn compute_self_hash(
    circuit: CircuitRc,
    hash_child_count: bool,
    hash_child_shapes: bool,
    hash_name: bool,
) -> HashBytes {
    let mut m = blake3::Hasher::new();
    for l in &circuit.info().shape {
        m.update(&l.to_le_bytes());
    }
    m.update(uuid!("92814fb9-3aa0-489c-b016-0f936941535b").as_bytes());
    if hash_name {
        m.update(circuit.name().unwrap_or("").as_bytes());
    }
    m.update(uuid!("6261daa8-0085-46f7-9f38-b085601fa628").as_bytes());
    if hash_child_count {
        m.update(&circuit.children().count().to_le_bytes());
    }
    m.update(uuid!("c7034aef-2179-4afa-9b90-c9abfcd1405d").as_bytes());
    if hash_child_shapes {
        for x in circuit.children() {
            for l in x.shape() {
                m.update(&l.to_le_bytes());
            }
            m.update(uuid!("17519b66-2332-450e-bdb2-bf893f8ed699").as_bytes());
        }
    }
    m.update(uuid!("e95b4d23-0077-4f57-a993-224454cb8570").as_bytes());
    circuit.compute_self_only_hash(&mut m);
    m.finalize().into()
}

const SAME_SELF_COLOR: Lazy<CliColor> = Lazy::new(|| clicolor!(Blue));
const SAME_COLOR: CliColor = CliColor::NONE;
const NEW_COLOR: Lazy<CliColor> = Lazy::new(|| clicolor!(Green));
const REMOVED_COLOR: Lazy<CliColor> = Lazy::new(|| clicolor!(Red));

#[pyfunction(
    options = "Default::default()",
    require_child_count_same = "true",
    require_child_shapes_same = "false",
    require_name_same = "true",
    print_legend = "true"
)]
pub fn diff_circuits(
    new: CircuitRc,
    old: CircuitRc,
    options: PrintOptions,
    require_child_count_same: bool,
    require_child_shapes_same: bool,
    require_name_same: bool,
    print_legend: bool,
) -> Result<String> {
    let mut options = options;
    options.bijection = false;
    let mut result = "".to_owned();
    let mut seen_diffs: HashMap<(CircuitRc, CircuitRc), String> = HashMap::default();
    let mut seen_independent: HashMap<CircuitRc, String> = HashMap::default();
    fn recurse(
        new: CircuitRc,
        old: CircuitRc,
        result: &mut String,
        options: &PrintOptions,
        last_child_stack: Vec<bool>,
        require_child_count_same: bool,
        require_child_shapes_same: bool,
        require_name_same: bool,
        seen_diffs: &mut HashMap<(CircuitRc, CircuitRc), String>,
        seen_indep: &mut HashMap<CircuitRc, String>,
    ) -> Result<()> {
        let diffkey = (new.clone(), old.clone());
        if let Some(id) = seen_diffs.get(&diffkey) {
            result.push_str(&indent(id.clone(), last_child_stack.len() * 2));
            result.push('\n');
            return Ok(());
        }
        let id = seen_diffs.len();

        if new == old {
            let mut new_options = options.clone();
            new_options.colorer = Some(PrintOptions::fixed_color(SAME_COLOR));
            let idstr = color(&format!(" # same {}", id), SAME_COLOR);
            let child_printed = new_options.repr(new.clone())?;
            let child_printed =
                once(&(child_printed.lines().next().unwrap().to_owned() + &idstr) as &str)
                    .chain(child_printed.lines().skip(1))
                    .join("\n");
            result.push_str(&indent(child_printed, last_child_stack.len() * 2));
            result.push_str("\n");
            seen_diffs.insert(diffkey.clone(), idstr);
            return Ok(());
        }
        if compute_self_hash(
            new.clone(),
            require_child_count_same,
            require_child_shapes_same,
            require_name_same,
        ) == compute_self_hash(
            old.clone(),
            require_child_count_same,
            require_child_shapes_same,
            require_name_same,
        ) {
            let line_prefix = if let Some(name) = new.name() {
                name.to_owned() + " "
            } else {
                "".to_owned()
            };

            result.push_str(&indent(
                color(
                    &format!("{}{}", line_prefix, options.repr_line_info(new.clone())?),
                    *SAME_SELF_COLOR,
                ),
                last_child_stack.len() * 2,
            ));
            let idstr = color(&format!(" # changed {}", id), *SAME_SELF_COLOR);
            result.push_str(&idstr);
            seen_diffs.insert(diffkey.clone(), idstr);
            result.push_str("\n");

            assert_eq!(new.children().count(), old.children().count());
            for (i, (new_child, old_child)) in zip(new.children(), old.children()).enumerate() {
                let new_child_stack: Vec<bool> = last_child_stack
                    .iter()
                    .cloned()
                    .chain(std::iter::once(i == new.children().count()))
                    .collect();
                recurse(
                    new_child,
                    old_child,
                    result,
                    options,
                    new_child_stack,
                    require_child_count_same,
                    require_child_shapes_same,
                    require_name_same,
                    seen_diffs,
                    seen_indep,
                )?;
            }
            return Ok(());
        }
        let mut new_options = options.clone();
        new_options.colorer = Some(PrintOptions::fixed_color(*NEW_COLOR));
        result.push_str(&indent(
            new_options.repr(new.clone())?,
            last_child_stack.len() * 2,
        ));
        result.push_str("\n");

        let mut new_options = options.clone();
        new_options.colorer = Some(PrintOptions::fixed_color(*REMOVED_COLOR));
        result.push_str(&indent(
            new_options.repr(old.clone())?,
            last_child_stack.len() * 2,
        ));
        result.push_str("\n");

        Ok(())
    }
    recurse(
        new,
        old,
        &mut result,
        &options,
        vec![],
        require_child_count_same,
        require_child_shapes_same,
        require_name_same,
        &mut seen_diffs,
        &mut seen_independent,
    )?;
    if print_legend {
        if &result[result.len() - 1..] != "\n" {
            result.push('\n');
        }
        write!(
            result,
            "{} {} {} {}\n",
            color("Black: Same as original", CliColor::NONE),
            color("Blue: Children changed", *SAME_SELF_COLOR),
            color("Green: New", *NEW_COLOR),
            color("Red: Removed", *REMOVED_COLOR)
        )
        .unwrap();
    }
    Ok(result)
}
