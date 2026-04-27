from sklearn.metrics import accuracy_score, cohen_kappa_score
import pandas as pd
import streamlit as st

st.markdown("""##Aggregate your codes here

* Upload the coding results as a .csv file.
- Make sure that the coding decisions are in the column named "label"

""")

f1 = st.file_uploader("Upload coder 1's result")
#f2 = st.file_uploader("Upload coder 2's result")

try:
  coder1 = pd.read_csv(f1)
  st.write(coder1.describe())
except:
  pass
