use pyo3::prelude::*;
use pyo3::pyclass::CompareOp;
use serde::ser::{SerializeSeq, Serializer};
use serde::Serialize;
use serde_json::{Map, Value};
use sha2::{Digest, Sha256};
use std::cmp::Ordering;
use std::collections::{HashMap, HashSet};
use std::fmt;
use std::fs::{read_to_string, File};
use std::io::prelude::*;

use crate::column_schema;
use crate::column_schema::ColumnSchema;
use crate::logical_types::LogicalTypes;
use crate::primitive::Primitive;
#[derive(Serialize)]
struct FileAsset {
    features: Vec<Feature>,
    primitives: Vec<Primitive>,
}

#[pyclass]
#[derive(Debug, Eq, Serialize, Clone)]
pub struct Feature {
    #[pyo3(get, set)]
    pub name: String,
    pub id: String,
    pub schema: ColumnSchema,
    #[pyo3(get, set)]
    #[serde(serialize_with = "child_serialize")]
    pub base_features: Vec<Feature>,
    #[pyo3(get, set)]
    #[serde(serialize_with = "serialize_primitive")]
    pub generating_primitive: Option<Primitive>,
}

#[pymethods]
impl Feature {
    #[new]
    fn __init__(
        name: &str,
        lt: &str,
        st: &str,
        base_features: Option<Vec<Feature>>,
        generating_primitive: Option<Primitive>,
    ) -> Self {
        let lt = LogicalTypes::try_from(lt).unwrap_or(LogicalTypes::Unknown);
        let st = LogicalTypes::try_from(st).unwrap_or(LogicalTypes::Unknown);

        let dtype = ColumnSchema::new(lt, st);

        if base_features.is_some() ^ generating_primitive.is_some() {
            panic!("base_features and generating_primitive must be both None or both Some");
        }

        Feature::new(
            name.to_string(),
            Some(dtype),
            generating_primitive,
            base_features,
        )
    }
    fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "{}:{:?}:{:?}:{:?}",
            self.name,
            self.schema,
            self.generating_primitive,
            self.base_features
                .iter()
                .map(|x| &x.name)
                .collect::<Vec<_>>()
        ))
    }
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!(
            "{}:{:?}:{:?}:{:?}",
            self.name,
            self.schema,
            self.generating_primitive,
            self.base_features
                .iter()
                .map(|x| &x.name)
                .collect::<Vec<_>>()
        ))
    }

    #[staticmethod]
    fn save_features(features: Vec<Feature>, filename: &str) -> PyResult<()> {
        Feature::write_many_to_file(&features, filename);

        Ok(())
    }

    fn __richcmp__(&self, other: &Feature, _op: CompareOp) -> PyResult<bool> {
        // println!("{:?} == {:?}", self, other);
        Ok(self.equals(other))
    }
}

fn rec(
    features: &Vec<Feature>,
    feature_set: &mut HashSet<Feature>,
    primitive_set: &mut HashSet<Primitive>,
) {
    for f in features {
        feature_set.insert(f.clone());
        if let Some(p) = &f.generating_primitive {
            primitive_set.insert(p.clone());
        }
        rec(&f.base_features, feature_set, primitive_set);
    }
}

fn rec2(
    f: Value,
    feature_map: &HashMap<String, Map<String, Value>>,
    primitive_map: &HashMap<String, Primitive>,
) -> Feature {
    let name = f
        .as_object()
        .unwrap()
        .get("name")
        .unwrap()
        .as_str()
        .unwrap()
        .to_string();
    let id = f
        .as_object()
        .unwrap()
        .get("id")
        .unwrap()
        .as_str()
        .unwrap()
        .to_string();
    let schema_raw = f.as_object().unwrap().get("schema").unwrap().clone();

    let schema: ColumnSchema = serde_json::from_value(schema_raw).unwrap();
    let base_features = f
        .as_object()
        .unwrap()
        .get("base_features")
        .unwrap()
        .as_array()
        .unwrap()
        .clone();
    let generating_primitive_raw = f.as_object().unwrap().get("generating_primitive").unwrap();

    let generating_primitive = match generating_primitive_raw.clone() {
        Value::String(id) => {
            let primitive = primitive_map.get(&id.clone()).unwrap().clone();
            Some(primitive)
        }
        Value::Null => None,
        _ => panic!("Unexpected generating primitive"),
    };

    let base_features: Vec<Feature> = base_features
        .iter()
        .map(|x| {
            let id = x.as_str().unwrap().to_string();
            let feature = feature_map.get(&id).unwrap().clone();
            rec2(Value::Object(feature), feature_map, primitive_map)
        })
        .collect();

    Feature {
        name,
        id,
        schema,
        base_features,
        generating_primitive,
    }
}

impl Feature {
    pub fn new(
        name: String,
        schema: Option<ColumnSchema>,
        generating_primitive: Option<Primitive>,
        base_features: Option<Vec<Feature>>,
    ) -> Feature {
        let dtype: ColumnSchema = if generating_primitive.is_some() {
            generating_primitive.as_ref().unwrap().clone().return_type
        } else {
            schema.expect(format!("Error unwrapping schema in {}", name).as_str())
        };

        let base_features = base_features.unwrap_or(vec![]);

        Feature {
            name: name.clone(),
            id: Feature::gen_id(&name, &base_features, &generating_primitive),
            schema: dtype,
            base_features,
            generating_primitive,
        }
    }

    fn gen_id(
        name: &String,
        base_features: &Vec<Feature>,
        generating_primitive: &Option<Primitive>,
    ) -> String {
        let mut hasher = Sha256::new();
        if let Some(ref o) = generating_primitive {
            hasher.update(o.id.clone());

            let bf_ids = base_features
                .iter()
                .map(|x| x.id.clone())
                .collect::<Vec<_>>();
            if o.commutative {
                let mut bf_ids = bf_ids;
                bf_ids.sort();
                for id in bf_ids {
                    hasher.update(id);
                }
            } else {
                for id in bf_ids {
                    hasher.update(id);
                }
            }
        } else {
            hasher.update(name);
        }

        let r = format!("{:x}", hasher.finalize());

        r
    }

    pub fn equals(&self, other: &Feature) -> bool {
        // --> do I need this?
        self == other
    }

    pub fn flatten(features: &Vec<Feature>) -> (HashSet<Feature>, HashSet<Primitive>) {
        let mut feature_set: HashSet<Feature> = HashSet::new();
        let mut primitive_set: HashSet<Primitive> = HashSet::new();

        rec(features, &mut feature_set, &mut primitive_set);
        return (feature_set, primitive_set);
    }

    pub fn write_many_to_file(features: &Vec<Feature>, filename: &str) {
        let (all_features, all_primitives) = Feature::flatten(features);

        let fa = FileAsset {
            features: all_features.into_iter().collect(),
            primitives: all_primitives.into_iter().collect(),
        };
        let a = serde_json::to_string(&fa);

        match a {
            Ok(s) => {
                // let filename = format!(&filename);
                let mut file = File::create(filename).unwrap();
                // let p = format!("{}\n", s);
                file.write_all(s.as_bytes()).expect("Error writing to file");
            }
            Err(e) => println!("{}", e),
        }
    }

    pub fn write_to_file(&self) {
        let j = serde_json::to_string(self);

        println!("--- FEATURE AS JSON");
        match j {
            Ok(s) => {
                println!("{}", s);
                let filename = format!("{}.json", self.name);
                let mut file = File::create(filename).unwrap();
                let p = format!("{}\n", s);
                file.write_all(p.as_bytes()).expect("Error writing to file");
            }
            Err(e) => println!("{}", e),
        }
    }

    pub fn read_from_file(filename: &str) -> Vec<Feature> {
        let contents = read_to_string(filename).expect("Something went wrong reading the file");
        let asset: Value = serde_json::from_str(&contents[..]).unwrap();

        let primitives_raw = asset
            .as_object()
            .unwrap()
            .get("primitives")
            .unwrap()
            .clone();

        let primitives: Vec<Primitive> = serde_json::from_value(primitives_raw).unwrap();

        let primitive_map: HashMap<String, Primitive> = primitives
            .iter()
            .map(|x| (x.id.clone(), x.clone()))
            .collect();

        // dbg!(primitive_map);

        let features = asset
            .as_object()
            .unwrap()
            .get("features")
            .unwrap()
            .as_array()
            .unwrap();

        let feature_map: HashMap<String, Map<String, Value>> = features
            .iter()
            .map(|x| {
                let obj = x.as_object().unwrap();
                let id = obj.get("id").unwrap().as_str().unwrap().to_string();

                (id, obj.clone())
            })
            .collect();

        let hydrated_features: Vec<Feature> = features
            .iter()
            .map(|f| rec2(f.clone(), &feature_map, &primitive_map))
            .collect();

        hydrated_features
    }
}

fn child_serialize<S>(x: &Vec<Feature>, s: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
{
    let mut seq = s.serialize_seq(Some(x.len()))?;
    for element in x {
        seq.serialize_element(&element.id)?;
    }
    seq.end()
}

fn serialize_primitive<S>(x: &Option<Primitive>, s: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
{
    match *x {
        Some(ref value) => s.serialize_some(&value.id),
        None => s.serialize_none(),
    }
}

impl fmt::Display for Feature {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} : {:?}", self.name, self.schema)
    }
}

impl PartialOrd for Feature {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Feature {
    fn cmp(&self, other: &Self) -> Ordering {
        self.id.cmp(&other.id)
    }
}

impl PartialEq for Feature {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}

/// Creates a new Feature definition
///
/// # Example
/// ```
/// use rust_dfs::{create_feature, column_schema, primitive};
///
/// // create a base feature with logical_type:integer and semantic_tag:numeric
/// let f = create_feature!("f1", "integer", "numeric");
///
/// // create some base features
/// let bf1 = create_feature!("bf1", "integer", "numeric");
/// let bf2 = create_feature!("bf2", "integer", "numeric");
///
/// // create a primitive
/// let p = primitive!("GreaterThan", vec![], column_schema!["integer", "numeric"], false);
///
/// // create a feature that is derived from bf1 and bf2 and uses primitive p
/// let f1 = create_feature!("idx", p.clone(), [bf1.clone(), bf2.clone()]);
/// ```
#[macro_export]
macro_rules! create_feature {
    ($name:expr, $prim:expr, [$( $x:expr ),*] ) => {{
        use $crate::feature::Feature;
        let mut base_features: Vec<Feature> = Vec::new();
        $(
            base_features.push($x);
        )*

        Feature::new($name.to_string(), None, Some($prim), Some(base_features))
    }};
    ($name:expr, $col_schema:expr ) => {{
        use $crate::feature::Feature;
        Feature::new($name.to_string(), Some($col_schema), None, None)
    }};
    ($name:expr, $lt:expr, $st:expr) => {{
        use $crate::column_schema;
        use $crate::feature::Feature;

        let dtype = column_schema![$lt, $st];
        Feature::new($name.to_string(), Some(dtype), None, None)
    }};
}

pub fn generate_fake_features(n_features: i32) -> Vec<Feature> {
    let mut features: Vec<Feature> = vec![create_feature!("idx", "integer", "numeric")];

    for i in 0..(n_features - 1) {
        let name = format!("F_{}", i);
        features.push(create_feature!(name, "integer", "numeric"));
    }

    return features;
}

#[cfg(test)]
mod tests {
    use serde_json::{Map, Value};

    use super::*;
    use std::{
        collections::{HashMap, HashSet},
        fs,
    };

    use crate::{column_schema, input_set, primitive};

    #[test]
    fn test_eq1() {
        let bf1 = create_feature!("bf1", "integer", "index");
        let bf1a = create_feature!("bf1", "integer", "index");
        let bf2 = create_feature!("bf2", "integer", "index");

        // assert origin features with same name and datatypes are equal
        assert_eq!(bf1, bf1a);

        // assert origin features with different names are not equal
        assert_ne!(bf1, bf2);

        assert_eq!([bf1.clone(), bf2.clone()], [bf1.clone(), bf2.clone()]);
        assert_ne!([bf1.clone(), bf2.clone()], [bf2.clone(), bf1.clone()]);

        // assert we can hash features, and that equal features are condensed
        let s1 = HashSet::from([&bf1, &bf1a, &bf2]);

        println!("{:?}", s1.contains(&bf1));
        println!("{:?}", s1.contains(&bf1a));
        assert!(s1.len() == 2);
    }

    #[test]
    fn test_eq2() {
        // Create base features
        let bf1 = create_feature!("origin_1", "integer", "index");
        let bf2 = create_feature!("origin_2", "integer", "index");

        let inputs1 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type1 = column_schema!["integer", "numeric"];

        // Commutative is false, so order matters
        // result should be ["F1", "F3"], since "F2" is same as "F1"
        let p1 = primitive!("GreaterThan", inputs1, r_type1, false);

        let f1 = create_feature!("f1", p1.clone(), [bf1.clone(), bf2.clone()]);
        let f2 = create_feature!("f2", p1.clone(), [bf1.clone(), bf2.clone()]);
        let f3 = create_feature!("f3", p1.clone(), [bf2.clone(), bf1.clone()]);

        assert_eq!(f1, f2);
        assert_ne!(f1, f3);

        let s1 = HashSet::from([&f1, &f2, &f3]);

        assert!(s1.len() == 2);

        // ================================================================

        let inputs2 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type2 = column_schema!["integer", "numeric"];

        let p2 = primitive!("GreaterThan", inputs2, r_type2, true);

        // Commutative is true, so order doesn't matter
        // result should be ["f1a"]
        let f1a = create_feature!("f1a", p2.clone(), [bf1.clone(), bf2.clone()]);
        let f2a = create_feature!("f2a", p2.clone(), [bf1.clone(), bf2.clone()]);
        let f3a = create_feature!("f3a", p2.clone(), [bf2.clone(), bf1.clone()]);

        let s2 = HashSet::from([&f1a, &f2a, &f3a]);

        assert!(s2.len() == 1);

        let c1 = column_schema!["double", "numeric"];
        let c2 = column_schema!["none", "numeric"];

        let f1 = create_feature!("f1", c1.clone());
        let f2 = create_feature!("f2", c2.clone());

        let s3 = HashSet::from([&f1, &f2]);
        assert!(s3.len() == 2);
    }

    #[test]
    fn test_macro() {
        let inputs = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type = column_schema!["integer", "numeric"];

        let p = primitive!("GreaterThan", inputs, r_type, false);

        let a = create_feature!("a", "integer", "numeric");
        let b = create_feature!("b", "integer", "numeric");

        let f1 = create_feature!("reed", p.clone(), [a, b]);

        println!("{:?}", f1);
    }

    #[test]
    fn test_serialize() {
        let f = create_feature!("bf1", "integer", "index");

        let json = serde_json::to_string(&f).unwrap();

        let expected = r#"{"name":"bf1","id":"def64d725ecd4bc3fe5315e7eb56ac740603d1372bec6b8925527ba70b793c69","schema":{"logical_type":"Integer","semantic_tag":"Index"},"base_features":[],"generating_primitive":null}"#;

        assert!(json == expected.to_string());

        let bf1 = create_feature!("origin_1", "integer", "index");
        let bf2 = create_feature!("origin_2", "integer", "index");

        let inputs1 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type1 = column_schema!["integer", "numeric"];

        // Commutative is false, so order matters
        // result should be ["F1", "F3"], since "F2" is same as "F1"
        let p1 = primitive!("GreaterThan", inputs1, r_type1, false);

        let f1 = create_feature!("f1", p1.clone(), [bf1.clone(), bf2.clone()]);

        let json = serde_json::to_string(&f1).unwrap();

        let expected = r#"{"name":"f1","id":"fa15e4309253d1cb1c5a9a9a52ff307fcdfc11402bd913d3f27b9d4b40424888","schema":{"logical_type":"Integer","semantic_tag":"Numeric"},"base_features":["760538b502bd28c2875ff2d17fd5e24749df190ff6e49ccc44267ea07f404641","c70faa957d52eb965690b7e1a9a4ef5b0ea02848322b9b4421f2924402b9610b"],"generating_primitive":"e3a64445d604e1b5aab469e2c4d9b7a9504e1b9960341d4357f19ba8fa89189d"}"#;

        assert!(json == expected.to_string());
    }

    #[test]
    fn test_flatten() {
        let bf1 = create_feature!("origin_1", "integer", "index");
        let bf2 = create_feature!("origin_2", "integer", "index");

        let inputs1 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type1 = column_schema!["integer", "numeric"];

        // Commutative is false, so order matters
        // result should be ["F1", "F3"], since "F2" is same as "F1"
        let p1 = primitive!("GreaterThan", inputs1, r_type1, false);

        let f1 = create_feature!("f1", p1.clone(), [bf1.clone(), bf2.clone()]);

        let features = vec![f1];
        let (all_features, all_primitives) = Feature::flatten(&features);

        assert_eq!(all_features.len(), 3);
        assert_eq!(all_primitives.len(), 1);
    }

    #[test]
    fn test_save() {
        let test_filename = "test_features.json";
        let bf1 = create_feature!("origin_1", "integer", "index");
        let bf2 = create_feature!("origin_2", "integer", "index");

        let inputs1 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type1 = column_schema!["integer", "numeric"];

        // Commutative is false, so order matters
        // result should be ["F1", "F3"], since "F2" is same as "F1"
        let p1 = primitive!("GreaterThan", inputs1, r_type1, false);

        let f1 = create_feature!("f1", p1.clone(), [bf1.clone(), bf2.clone()]);

        let features = vec![f1];
        Feature::write_many_to_file(&features, test_filename);
        fs::remove_file(test_filename).unwrap();
    }

    #[test]
    fn test_read() {
        let test_filename = "test_features2.json";
        let bf1 = create_feature!("origin_1", "integer", "index");
        let bf2 = create_feature!("origin_2", "integer", "index");

        let inputs1 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type1 = column_schema!["integer", "numeric"];

        // Commutative is false, so order matters
        // result should be ["F1", "F3"], since "F2" is same as "F1"
        let p1 = primitive!("GreaterThan", inputs1, r_type1, false);

        let f1 = create_feature!("f1", p1.clone(), [bf1.clone(), bf2.clone()]);

        let features = vec![f1];
        Feature::write_many_to_file(&features, test_filename);

        let features = Feature::read_from_file(test_filename);

        fs::remove_file(test_filename).unwrap();

        assert_eq!(features.len(), 3);
    }
}
