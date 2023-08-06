use polars::df;
use polars::export::arrow::compute::filter;
use polars::prelude::*;
use std::collections::HashMap;

pub fn test_polars() {
    let solar_distance = HashMap::from([
        ("Mercury", 0.4),
        ("Venus", 0.7),
        ("Earth", 1.0),
        ("Mars", 1.5),
    ]);

    let df = df![
        "a" => [1, 2, 3, -22],
    ]
    .unwrap();

    println!("{:?}", df);
    // let filtered = df.lazy().filter(col("a").gt(lit(2))).collect().unwrap();
    // df.lazy().groupby([col("date")]);

    let a = col("a").cummax(false);

    let f = |x: &str| col(x).cummax(false);

    let df2 = df.lazy().select([col("a").abs()]).collect().unwrap();

    println!("{:?}", df2);
}

#[cfg(test)]
mod tests {
    use super::test_polars;
    #[test]
    fn test() {
        println!("Test");
        test_polars();
    }
}
