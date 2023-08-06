import polars as pl


def absolute(cols):
    return pl.col(cols[0]).abs()


def add_numeric(cols):
    return pl.map(cols, lambda s: s[0] + s[1])


def add_numeric_scalar(cols, scalar=0):
    return pl.col(cols[0]) + scalar


def logical_and(cols):
    return pl.map(cols, lambda s: s[0] and s[1])


def cosine(cols):
    return pl.col(cols[0]).cos()


def cum_count(cols):
    return pl.col(cols[0]).cumcount()


def cum_max(cols):
    return pl.col(cols[0]).cummax()


def cum_mean(cols):
    return pl.col(cols[0]).cumulative_eval(pl.element().mean())


def cum_min(cols):
    return pl.col(cols[0]).cummin()


def cum_sum(cols):
    return pl.col(cols[0]).cumsum()


def day_of_month(cols):
    return pl.col(cols[0]).dt.day()


def day_of_year(cols):
    return pl.col(cols[0]).dt.ordinal_day()


def diff(cols):
    return pl.col(cols[0]).diff()


def divide_by_feature(cols, scalar=1):
    return scalar / pl.col(cols[0])


def divide_numeric(cols):
    return pl.map(cols, lambda s: s[0] / s[1])


def divide_numeric_scalar(cols, scalar=1):
    return pl.col(cols[0]) / scalar


primitive_map = {
    "Absolute": absolute,
    "AddNumeric": add_numeric,
    "AddNumericScalar": add_numeric_scalar,
    "And": logical_and,
    "Cosine": cosine,
    "CumCount": cum_count,
    "CumMax": cum_max,
    "CumMean": cum_mean,
    "CumMin": cum_min,
    "CumSum": cum_sum,
    "DayOfMonth": day_of_month,
    "DayOfYear": day_of_year,
    "Diff": diff,
    "DivideByFeature": divide_by_feature,
    "DivideNumeric": divide_numeric,
    "DivideNumericScalar": divide_numeric_scalar,
}
