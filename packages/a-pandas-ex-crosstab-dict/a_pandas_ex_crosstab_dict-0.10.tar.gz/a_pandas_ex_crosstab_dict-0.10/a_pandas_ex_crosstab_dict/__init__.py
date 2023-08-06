from typing import Union

import pandas as pd
from pandas.core.frame import DataFrame


def crosstab(
    df: pd.DataFrame,
    maincolumn: Union[str, float, int],
    columns: Union[None, list] = None,
) -> dict:
    if not columns:
        columns = df.columns.to_list()

    return {
        pd.crosstab(df[maincolumn], df[x])
        .T.index.name: pd.crosstab(df[maincolumn], df[x])
        .T
        for x in [y for y in columns if y != maincolumn]
    }


def pd_add_crosstab_dict():
    DataFrame.ds_get_crosstab_dict = crosstab



