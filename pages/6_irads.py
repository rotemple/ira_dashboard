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

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


st.header('IRA Facebook Ad Dataset')
st.markdown('## Reference')
st.write("""Lindblad, P., Murphy, N., Pfister, D.S., Styer, M., Summers, E., and Yang, M. Internet Research Agency Ads Dataset. [data file]. Retrieved from https://mith.umd.edu/irads/data.zip.""")
df = load_csv('https://raw.githubusercontent.com/rotemple/irads/refs/heads/master/site/index.csv')
df.id = df.id.astype(str)
column = st.selectbox('Select Column to Search',[None] + df.columns.tolist())
query = st.text_input('Search by Keyword')
if column != None:
        df = search_dataframe(df,query.lower(),column)
        st.data_editor(df,column_config={
        "image": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots"
        )
    },
    hide_index=True,)
        csv = convert_df(df)
        #st.download_button("Press to Download Filtered CSV",csv,"file.csv","text/csv",key='download-csv')
        
elif column == None:
        st.data_editor(df,column_config={
        "image": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots"
        )
    },
    hide_index=True,
)
csv = convert_df(df)
st.download_button("Press to Download",csv,"file.csv","text/csv",key='download-csv')
        #st.dataframe(df)




