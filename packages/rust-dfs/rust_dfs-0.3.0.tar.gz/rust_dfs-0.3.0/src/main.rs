use polars::prelude::*;

fn example(df: &DataFrame) -> Result<DataFrame> {
    df.groupby(["cats"])?
        .agg(&[("val", &["n_unique", "sum", "min"])])
}

fn join_example() {
    let df1: DataFrame = df!("Fruit" => &["Apple", "Banana", "Pear"],
                         "Phosphorus (mg/100g)" => &[11, 22, 12])
    .unwrap();
    let df2: DataFrame = df!("Name" => &["Apple", "Banana", "Pear"],
                         "Potassium (mg/100g)" => &[107, 358, 115])
    .unwrap();

    let df3: DataFrame = df1
        .join(&df2, ["Fruit"], ["Name"], JoinType::Inner, None)
        .unwrap();
    assert_eq!(df3.shape(), (3, 3));
    println!("{}", df3);
}

fn main() {
    println!("dave");

    let df1: DataFrame = df!(
        "cats" => &["A", "A", "A", "B", "B", "C"],
        "val" => &[3, 3, 3, 4, 4, 3]
    )
    .unwrap();

    let df2 = example(&df1);

    dbg!(df1, df2);

    // join_example();
}
