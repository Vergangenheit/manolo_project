import pandas as pd
from pandas import DataFrame, ExcelWriter
import numpy as np
from typing import List, Dict, Tuple, Union
import itertools
import pathlib
import openpyxl
from io import BytesIO
from tempfile import SpooledTemporaryFile

PACKAGE_ROOT = pathlib.Path().resolve()


# df = pd.read_excel(PACKAGE_ROOT / 'data/TM_Parco_51.xlsx', usecols=list(range(5)))

def process(file: Union[str, SpooledTemporaryFile], save_df: bool = False):
    # read file
    # df = pd.read_excel(file, usecols=list(range(5)))
    df: DataFrame = pd.read_excel(file)
    # put column unique data them in lists
    lists: Dict = {}
    for col in df.columns:
        lists[col]: List = df[col].dropna().unique().tolist()
    # extract list of lists of possible combinations
    res: List[Tuple] = list(itertools.product(*list(lists.values())))

    # do a couple of logic checks
    for r in res:
        assert len(r) == len(df.columns)
    assert len([' '.join(r) for r in res]) == len(set(' '.join(r) for r in res))
    # convert results into dataframe
    result: DataFrame = pd.DataFrame(res)
    if save_df:
        name: str = '../data/results.xlsx'
        # result.to_excel(pathlib.Path(file_path).resolve().parent / 'results.xlsx')
        result.to_excel(name)

    # return result


def to_excel(df: DataFrame) -> bytes:
    output: BytesIO = BytesIO()
    writer: ExcelWriter = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data: bytes = output.getvalue()
    return processed_data


if __name__ == "__main__":
    process(PACKAGE_ROOT / 'data/TM_Parco_51.xlsx', save_df=True)
