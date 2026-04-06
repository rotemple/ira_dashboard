import streamlit as st
import pandas as pd
import re
import itertools
from collections import Counter

def flatten_list(somelist):
        if any(isinstance(el, list) for el in somelist) == False:
            return somelist
        flat_list = list(itertools.chain(*somelist))
        return flat_list

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def search_dataframe(dataframe,query,column):
    dataframe[column] = dataframe[column].str.lower()
    dataframe['search'] = dataframe[column].str.contains(query)
    return dataframe[dataframe['search'] == True]

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def load_csv(url):
  return pd.read_csv(url)
df = load_csv('https://raw.githubusercontent.com/rotemple/irads/refs/heads/master/site/index.csv')
column = st.selectbox('Select Column to Search',df.columns.tolist())
query = st.text_input('Search by Keyword')
if column:
        df = st.dataframe(search_dataframe(df,query,column))
else:
        df
st.write(df)



