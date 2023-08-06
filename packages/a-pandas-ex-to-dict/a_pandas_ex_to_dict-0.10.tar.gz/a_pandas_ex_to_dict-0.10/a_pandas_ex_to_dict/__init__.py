import pandas as pd
from pandas.core.frame import DataFrame


def dictify(df, cols):
    # https://stackoverflow.com/a/74810722/15096247
    if not cols:
        return len(df)
    return {k: dictify(g, cols[1:]) for k, g in df.groupby(cols[0])}


def pandas_to_nested_dict(df, cols=None):
    if cols is None:
        return dictify(df, list(df.columns.to_list())[: len(df.columns) - 2])
    else:
        return dictify(df, cols)


def pd_add_df_to_nested_dict():
    DataFrame.d_to_nested_dict = pandas_to_nested_dict

