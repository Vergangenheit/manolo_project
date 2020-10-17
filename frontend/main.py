import streamlit as st
import requests
import pandas as pd
import itertools
import base64
from io import BytesIO


def process(file, save_df: bool = False):
    # read file
    # df = pd.read_excel(file, usecols=list(range(5)))
    df = pd.read_excel(file)
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
        name = '/storage/results.xlsx'
        # result.to_excel(pathlib.Path(file_path).resolve().parent / 'results.xlsx')
        result.to_excel(name)

    return result


def to_excel(df: pd.DataFrame):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df: pd.DataFrame):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download excel file</a>'  # decode b'abc' => abc


st.set_option("deprecation.showfileUploaderEncoding", False)

# defines an h1 header
st.title("Create all possibile combinations web app")

# displays a file uploader widget
excel_file = st.file_uploader("Choose an excel file")

if st.button("Combinations"):
    if excel_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        dataframe = process(excel_file)

        st.write(dataframe)
        st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)
