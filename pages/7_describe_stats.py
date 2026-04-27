from sklearn.metrics import accuracy_score, cohen_kappa_score
import pandas as pd
import streamlit as st

st.markdown("""##Aggregate your codes here

* Upload the coding results as a .csv file.
- Make sure that the coding decisions are in the column named "label"

""")

f1 = st.file_uploader("Upload coder 1's result")
#f2 = st.file_uploader("Upload coder 2's result")
coder1 = pd.read_csv(f1, encoding='latin1')
rows = st.selectbox('Select a Row Value',coder1.columns)
columns = st.selectbox('Select a Columns Value',coder1.columns)
values = st.selectbox('Select the Column You Want to Sum',coder1.columns)
try:
  table = pd.pivot_table(
      coder1, values=values, index=[rows],columns=[columns], aggfunc="sum"
  )
  st.write(table)
except:
  pass
