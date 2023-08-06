import pandas as pd
from typing import Sequence

def describe(**kwargs):
    """each value must be a list"""
    dfs = []
    for k, data in kwargs.items():
        if not isinstance(data, Sequence): continue
        dfs.append(pd.DataFrame({k: data}).describe())
    return pd.merge(*dfs, left_index=True, right_index=True)
