from typing import Union

import pandas as pd
from pandas.core.frame import DataFrame, Series


def series_to_dataframe_convert(
    df: Union[pd.DataFrame, pd.Series]
) -> (Union[pd.DataFrame, pd.Series], bool):
    isseries_ = False
    dataf = df.copy()
    if isinstance(dataf, pd.Series):
        isseries_ = True
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
    return dataf, isseries_


def enumerate_groups(dframe, enumerated_column, column_to_enumerate):
    col = column_to_enumerate
    gdf, isseries = series_to_dataframe_convert(dframe)
    if isseries:
        col = gdf.columns[0]
    soind = gdf[col].value_counts().index.sort_values(0)
    soind1_ = soind[-1]
    soind2_ = soind[-2]
    nafill = soind1_ + soind2_
    gdf = gdf.sort_values(by=col)
    df = gdf.copy()
    df[col] = df[col].fillna(nafill)
    dfgr = df.groupby(col, dropna=False)[col]
    ppa = dfgr.apply(
        lambda x: (
            [list(dfgr.groups.keys()).index(x.name)] * len(dfgr.groups.get(x.name))
        )
    )
    wholeg = ppa.reset_index(drop=True).explode(0).reset_index(drop=True)
    wholeg.index = df.index.__array__().copy()
    gdf[enumerated_column] = wholeg.copy()
    return gdf


def pd_add_enumerate_group():
    DataFrame.ds_enumerate_groups = enumerate_groups
    Series.ds_enumerate_groups = enumerate_groups


