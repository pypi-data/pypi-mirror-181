import random
from .utils import semantic_tag_mapping, logical_type_mapping
from woodwork.logical_types import Ordinal
import pandas as pd
import polars as pl
from datetime import datetime as dt


def flatten(xss):
    return [x for xs in xss for x in xs]


def randomize(v):
    random.seed(10)
    h = v.copy()
    random.shuffle(h)
    return h


def gen_data_dict(value, nrows: int, start_idx=0, n_features=5) -> dict:
    values = [value] * nrows
    if isinstance(value, list):
        values = flatten(values)

    data = {f"F_{start_idx + n}": randomize(values)[:nrows] for n in range(n_features)}

    return data


def generate_pandas_fake_dataframe(
    n_rows=10, col_defs=[("Numeric", 2)], time_index=False
):
    def gen_type_dict(lt, st, start_idx=0, n_features=5):
        lt_dict = {}
        st_dict = {}
        for n in range(n_features):
            name = f"F_{start_idx + n}"
            if lt:
                lt_dict[name] = lt
            if st:
                st_dict[name] = st
        return lt_dict, st_dict

    dataframes = [pd.DataFrame({"idx": range(n_rows)})]

    lt_dict = {}
    st_dict = {}
    starting_col = 0
    for typ, n_cols in col_defs:
        logical_type = None
        semantic_tag = None
        if typ in logical_type_mapping:
            logical_type = typ
            values = logical_type_mapping[typ]
            if logical_type == "Ordinal":
                logical_type = Ordinal(order=values)
        elif typ in semantic_tag_mapping:
            semantic_tag = typ.lower()
            values = semantic_tag_mapping[typ]
        else:
            values = typ

        df_tmp = pd.DataFrame(gen_data_dict(values, n_rows, starting_col, n_cols))
        dataframes.append(df_tmp)
        lt_dict_tmp, st_dict_tmp = gen_type_dict(
            logical_type, semantic_tag, starting_col, n_cols
        )
        lt_dict.update(lt_dict_tmp)
        st_dict.update(st_dict_tmp)

        starting_col += n_cols

    df = pd.concat(dataframes, axis=1)

    other_kwargs = {}
    if time_index:
        df["t_idx"] = pd.date_range(end=dt(2020, 1, 1, 12, 0, 0), periods=n_rows)
        lt_dict["t_idx"] = "Datetime"
        other_kwargs["time_index"] = "t_idx"

    df.ww.init(
        name="nums",
        index="idx",
        logical_types=lt_dict,
        semantic_tags=st_dict,
        **other_kwargs,
    )

    return df


def generate_polars_fake_dataframe(n_rows=10, col_defs=[("Numeric", 2)]):

    data_dict = {"idx": range(n_rows)}
    starting_col = 0
    for typ, n_cols in col_defs:
        if typ in logical_type_mapping:
            values = logical_type_mapping[typ]
        elif typ in semantic_tag_mapping:
            values = semantic_tag_mapping[typ]
        else:
            values = typ

        ddict_tmp = gen_data_dict(values, n_rows, starting_col, n_cols)
        data_dict.update(ddict_tmp)
        starting_col += n_cols

    df = pl.DataFrame(data_dict)

    return df
