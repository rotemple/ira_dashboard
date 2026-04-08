from sklearn.metrics import accuracy_score, cohen_kappa_score
import pandas as pd
import streamlit as st

st.markdown("""##Calculate inter-rater agreement using Cohen's Kappa
This app calculates Cohen's Kappa for 2 coders
Instructions:
- Upload the coding results from Coder 1 and Coder 2 as .csv files.
-- Make sure that the coding decisions are in the column named "label"
-- Make sure code decisions are aligned between the 2 .csv files

f1 = st.file_uploader('Upload coder 1's result')
f2 = st.file_uploader('Upload coder 2's result')

coder1 = pd.read_csv(f1, usecols=['label'])
coder2 = pd.read_csv(f2, usecols=['label'])

st.markdown("""## Cohen's Kappa Score"""
st.write(cohen_kappa_score(coder1,coder2)
