use chrono::prelude::*;
use chrono::Duration;
use fake::faker::internet::raw::FreeEmail;
use fake::faker::lorem::en::*;
use fake::locales::*;
use fake::Fake;
use polars::prelude::*;
use rand::prelude::*;
use rand::thread_rng;

enum LogicalType {
    Boolean,
    BooleanNullable,
    Categorical,
    Datetime,
    Double,
    Integer,
    IntegerNullable,
    EmailAddress,
    // LatLong,
    NaturalLanguage,
    Ordinal,
    URL,
}

fn gen_datetime(n_rows: usize) -> Vec<String> {
    let dt = Utc::now();
    let mut v = vec![];
    for i in 0..n_rows {
        let a = dt + Duration::days((i as i64) - (n_rows as i64));

        v.push(a.to_string());
    }

    return v;
}

fn gen_natural_language(n_rows: usize) -> Vec<String> {
    let mut v = vec![];
    for _ in 0..n_rows {
        v.push(Sentence(1..20).fake());
    }

    return v;
}

fn gen_url(n_rows: usize) -> Vec<String> {
    let mut v = vec![];
    for _ in 0..n_rows {
        let w: String = Word().fake();
        v.push(format!("https://{}.com", w));
    }

    return v;
}

fn gen_double(n_rows: usize) -> Vec<f64> {
    let mut v = vec![];
    for _ in 0..n_rows {
        let mut rng = thread_rng();
        v.push(rng.gen_range(0.0..100.0));
    }

    return v;
}

fn gen_integer(n_rows: usize) -> Vec<i64> {
    let mut v = vec![];
    for _ in 0..n_rows {
        let mut rng = thread_rng();
        v.push(rng.gen_range(0..100));
    }

    return v;
}

fn gen_integer_nullable(n_rows: usize) -> Vec<Option<i64>> {
    let mut v = vec![];
    for _ in 0..n_rows {
        let mut rng = thread_rng();
        v.push(Some(rng.gen_range(0..100)));
    }

    return v;
}

fn gen_email_address(n_rows: usize) -> Vec<Option<String>> {
    let mut v = vec![];
    for _ in 0..n_rows {
        v.push(Some(FreeEmail(EN).fake()));
    }

    return v;
}

fn gen_ordinal(n_rows: usize) -> Vec<Option<i64>> {
    let mut v = vec![];
    for _ in 0..n_rows {
        let mut rng = thread_rng();
        v.push(Some(rng.gen_range(0..100)));
    }

    return v;
}

fn gen_bool(n_rows: usize) -> Vec<bool> {
    let mut d = vec![];
    for _ in 0..n_rows {
        let a: bool = rand::random();
        d.push(a);
    }
    return d;
}

fn gen_bool_nullable(n_rows: usize) -> Vec<Option<bool>> {
    let mut d = vec![];
    for _ in 0..n_rows {
        let a: f32 = rand::random();

        if a > 0.66 {
            d.push(Some(true));
        } else if a > 0.33 {
            d.push(Some(false))
        } else {
            d.push(None)
        }
    }
    return d;
}

fn gen_categorical(n_rows: usize) -> Vec<String> {
    let mut d = vec![];
    for _ in 0..n_rows {
        let a: f32 = rand::random();
        if a > 0.66 {
            d.push("A".to_string());
        } else if a > 0.33 {
            d.push("B".to_string())
        } else {
            d.push("C".to_string())
        }
    }
    return d;
}

fn main() {
    let inputs = vec![
        LogicalType::Boolean,
        LogicalType::BooleanNullable,
        LogicalType::Categorical,
        LogicalType::Datetime,
        LogicalType::Double,
        LogicalType::Integer,
        LogicalType::IntegerNullable,
        LogicalType::EmailAddress,
        LogicalType::NaturalLanguage,
        LogicalType::Ordinal,
        LogicalType::URL,
    ];

    let n_rows = 1000;

    // let a = random_vec(
    //     vec!["A".to_string(), "B".to_string(), "C".to_string()],
    //     n_rows,
    // );

    let series: Vec<Series> = inputs
        .iter()
        .map(|a| match a {
            LogicalType::Boolean => Series::new("bool", gen_bool(n_rows)),
            LogicalType::BooleanNullable => Series::new("bool_null", gen_bool_nullable(n_rows)),
            LogicalType::Categorical => Series::new("cat", gen_categorical(n_rows)),
            LogicalType::Datetime => Series::new("dt", gen_datetime(n_rows)),
            LogicalType::Double => Series::new("dbl", gen_double(n_rows)),
            LogicalType::Integer => Series::new("int", gen_integer(n_rows)),
            LogicalType::IntegerNullable => Series::new("int_null", gen_integer_nullable(n_rows)),
            LogicalType::EmailAddress => Series::new("email", gen_email_address(n_rows)),
            LogicalType::NaturalLanguage => Series::new("nl", gen_natural_language(n_rows)),
            LogicalType::Ordinal => Series::new("ord", gen_ordinal(n_rows)),
            LogicalType::URL => Series::new("url", gen_url(n_rows)),
        })
        .collect();

    let mut df = DataFrame::new(series).unwrap();

    let mut file = std::fs::File::create("data.csv").unwrap();

    CsvWriter::new(&mut file).finish(&mut df).unwrap();
}
