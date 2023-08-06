import featuretools as ft
import json
from featuretools.primitives.utils import (
    get_aggregation_primitives,
    get_transform_primitives,
)
from .rust_dfs import Primitive, Feature
import numpy as np
from datetime import datetime as dt


tag_map = {
    "numeric": "Numeric",
    "category": "Categorical",
    "categorical": "Categorical",
    "time_index": "TimeIndex",
    "timeindex": "TimeIndex",
    "foreign_key": "ForeignKey",
    "foreignkey": "ForeignKey",
    "date_of_birth": "DateOfBirth",
    "dateofbirth": "DateOfBirth",
    "index": "Index",
}


def convert_primitive(ft_primitive):
    fp_dict = serialize_primitive(ft_primitive(), "transform")

    if fp_dict is None:
        return None

    input_types = []
    for y in fp_dict["input_types"]:
        input_types.append([(x["logical_type"], x["semantic_tag"]) for x in y])

    return Primitive(
        fp_dict["type"],
        fp_dict["module"],
        "transform",
        fp_dict["commutative"],
        input_types,
        (
            fp_dict["return_type"]["logical_type"],
            fp_dict["return_type"]["semantic_tag"],
        ),
    )


def convert_primitives(ft_primitives):
    out = []
    for fp in ft_primitives:
        p = convert_primitive(fp)

        if p:
            out.append(p)
    return out


def dataframe_to_features(df):
    features = []
    for name, col in df.ww.schema.columns.items():
        col_dict = col_to_dict(col, "unknown")
        f = Feature(
            name,
            col_dict["logical_type"],
            col_dict["semantic_tag"],
        )

        features.append(f)
    return features


def convert_features(f_features):
    f_features = f_features.copy()

    all_features = {}
    while f_features:
        f = f_features.pop(0)

        if len(f.base_features) == 0:
            all_features[f._name] = convert_feature(f)
        elif all([x._name in all_features for x in f.base_features]):

            base_features = [all_features[x._name] for x in f.base_features]
            all_features[f._name] = convert_feature(f, base_features)
        else:
            for bf in f.base_features:
                if bf._name not in all_features:
                    f_features.append(bf)
            f_features.append(f)

    return all_features


def get_primitive_return_type(primitive):
    if primitive.return_type is None:
        return_type = primitive.input_types[0]
        if isinstance(return_type, list):
            return_type = return_type[0]
    else:
        return_type = primitive.return_type

    return return_type


def convert_feature(f_feature, base_features=None):

    name = f_feature._name

    primitive = type(f_feature.primitive)
    r_primitive = convert_primitive(primitive)

    if hasattr(f_feature, "return_type"):
        col_dict = col_to_dict(f_feature.return_type, "unknown")
    else:
        col_dict = col_to_dict(get_primitive_return_type(primitive), "unknown")

    return Feature(
        name,
        col_dict["logical_type"] or "Any",
        col_dict["semantic_tag"] or "Any",
        base_features,
        r_primitive,
    )


def col_to_dict(col, unknown_type="any"):

    if col.logical_type:
        lt_name = type(col.logical_type).__name__
    else:
        lt_name = unknown_type

    semantic_tags = list(col.semantic_tags)

    if len(semantic_tags):
        # todo: handle multiple semantic tags
        semantic_tags = tag_map[semantic_tags[0].lower()]
    else:
        semantic_tags = unknown_type

    return {
        "logical_type": lt_name,
        "semantic_tag": semantic_tags,
    }


def get_input_types(input_types):
    if not isinstance(input_types[0], list):
        input_types = [input_types]

    out = []
    for input_type_set in input_types:
        out_set = []
        for input_type in input_type_set:
            out_set.append(col_to_dict(input_type))
        out.append(out_set)
    return out


def serialize_primitive(primitive, function_type):
    """build a dictionary with the data necessary to construct the given primitive"""
    args_dict = {name: val for name, val in primitive.get_arguments()}
    cls = type(primitive)

    if type(primitive) == ft.primitives.base.PrimitiveBase:
        return None

    return_type = get_primitive_return_type(primitive)
    return {
        "type": cls.__name__,
        "module": cls.__module__,
        "arguments": args_dict,
        "input_types": get_input_types(primitive.input_types),
        "return_type": col_to_dict(return_type),
        "function_type": function_type,
        "commutative": primitive.commutative,
    }


logical_type_mapping = {
    "Boolean": [True, False],
    "BooleanNullable": [True, False, np.nan],
    "Datetime": [dt(2020, 1, 1, 12, 0, 0), dt(2020, 6, 1, 12, 0, 0)],
    "EmailAddress": ["john.smith@example.com", "sally.jonex@example.com"],
    "LatLong": [(1, 2), (3, 4)],
    "NaturalLanguage": ["This is sentence 1", "This is sentence 2"],
    "Ordinal": [1, 2, 3],
    "URL": ["https://www.example.com", "https://www.example2.com"],
}

semantic_tag_mapping = {
    "Categorical": ["A", "B", "C"],
    "DateOfBirth": [dt(2020, 1, 1, 12, 0, 0), dt(2020, 6, 1, 12, 0, 0)],
    "ForeignKey": [1, 2],
    "Numeric": [1.2, 2.3, 3.4],
    "TimeIndex": [dt(2020, 1, 1, 12, 0, 0), dt(2020, 6, 1, 12, 0, 0)],
}


def df_to_es(df):
    es = ft.EntitySet(id="nums")
    es.add_dataframe(df, "nums", index="idx")

    return es


def serialize_feature(f):
    base_features = [x._name for x in f.base_features]
    cls = type(f.primitive)
    primitive_name = cls.__name__
    n2 = "_".join(base_features)

    return {
        "name": f"{primitive_name}_{n2}",
        "base_features": base_features,
        "generating_primitive": primitive_name,
        "commutative": cls.commutative,
    }


def save_features(features, fname="all_features.json"):
    out = []
    for f in features:
        out.append(serialize_feature(f))

    json.dump(out, open(fname, "w"))


def serialize_all_primitives():
    transform_prim_dict = get_transform_primitives()
    aggregation_prim_dict = get_aggregation_primitives()

    trans_prims = list(transform_prim_dict.values())

    agg_prims = list(aggregation_prim_dict.values())

    all_prims = []

    for p in trans_prims:
        all_prims.append(serialize_primitive(p(), "transform", "any"))

    for p in agg_prims:
        all_prims.append(serialize_primitive(p(), "aggregation", "any"))

    json.dump(all_prims, open("primitives.json", "w"))
