use super::Feature;
use std::hash::{Hash, Hasher};

impl Hash for Feature {
    fn hash<H: Hasher>(&self, state: &mut H) {
        match self.generating_primitive {
            Some(ref p1) => {
                p1.hash(state);

                let mut v = self.base_features.clone();
                v.sort();

                v.hash(state);
            }
            None => {
                self.name.hash(state);
            }
        }
    }
}
