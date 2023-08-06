use std::collections::HashSet;

use pyo3::prelude::*;

use super::Feature;

#[pyfunction]
pub fn compare_featuresets(
    features1: Vec<Feature>,
    features2: Vec<Feature>,
) -> (Vec<Feature>, Vec<Feature>) {
    let features1: HashSet<Feature> = HashSet::from_iter(features1.iter().cloned());

    let features2: HashSet<Feature> = HashSet::from_iter(features2.iter().cloned());

    let diff1: Vec<Feature> = features1.difference(&features2).cloned().collect();

    let diff2: Vec<Feature> = features2.difference(&features1).cloned().collect();

    return (diff1, diff2);
}

#[cfg(test)]
mod tests {
    use super::compare_featuresets;
    use crate::{column_schema, create_feature, input_set, primitive};

    #[test]
    fn test_compare_featuresets() {
        let bf1 = create_feature!("bf1", "integer", "index");
        let bf2 = create_feature!("bf2", "integer", "index");

        let inputs1 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type1 = column_schema!["integer", "numeric"];

        // Commutative is false, so order matters
        let p1 = primitive!("GreaterThan", inputs1, r_type1, false);

        let f1 = create_feature!("f1", p1.clone(), [bf1.clone(), bf2.clone()]);
        let f2 = create_feature!("f2", p1.clone(), [bf1.clone(), bf2.clone()]);
        let f3 = create_feature!("f2", p1.clone(), [bf2.clone(), bf1.clone()]);

        let (d1, d2) = compare_featuresets(vec![f1.clone()], vec![f2.clone()]);

        assert!(d1.len() == 0);
        assert!(d2.len() == 0);

        let (d1, d2) = compare_featuresets(vec![f1.clone()], vec![f3.clone()]);

        assert!(d1.len() == 1);
        assert!(d2.len() == 1);
    }
}
