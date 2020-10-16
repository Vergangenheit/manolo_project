import pandas as pd
import numpy as np
from typing import List
import itertools
import pathlib
import openpyxl

PACKAGE_ROOT = pathlib.Path().resolve()



# df = pd.read_excel(PACKAGE_ROOT / 'data/TM_Parco_51.xlsx', usecols=list(range(5)))


def run(file_path: str, save_df: bool = False):
    # read file
    df = pd.read_excel(file_path, usecols=list(range(5)))
    # put column unique data them in lists
    lists = {}
    for col in df.columns:
        lists[col] = df[col].dropna().unique().tolist()
    # extract list of lists of possible combinations
    res = list(itertools.product(*list(lists.values())))

    # do a couple of logic checks
    for r in res:
        assert len(r) == len(df.columns)
    assert len([' '.join(r) for r in res]) == len(set(' '.join(r) for r in res))
    # convert results into dataframe
    result = pd.DataFrame(res)
    if save_df:
        result.to_excel(pathlib.Path(file_path).resolve().parent / 'results.xlsx')

    return result


if __name__ == "__main__":
    res = run(PACKAGE_ROOT / 'data/TM_Parco_51.xlsx', save_df=True)
    print(res)
