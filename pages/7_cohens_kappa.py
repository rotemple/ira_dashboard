from sklearn.metrics import accuracy_score, cohen_kappa_score
import pandas as pd
import streamlit as st

st.markdown("""##Calculate inter-rater agreement using Cohen's Kappa
This app calculates Cohen's Kappa for 2 coders
Instructions:
* Upload the coding results from Coder 1 and Coder 2 as .csv files.
- Make sure that the coding decisions are in the column named "label"
- Make sure code decisions are aligned between the 2 .csv files (i.e., coders have coded the same rows in the spreadsheet)
""")

f1 = st.file_uploader("Upload coder 1's result")
f2 = st.file_uploader("Upload coder 2's result")

try:
  coder1 = pd.read_csv(f1, usecols=['label']).dropna()
  coder2 = pd.read_csv(f2, usecols=['label']).dropna()

  st.markdown('## Coded Data')
  st.dataframe(coder1)
  st.dataframe(coder2)
  st.markdown('## Accuracy')
  
  st.write('Accuracy: 'accuracy_score(coder1.label.tolist(), coder2.label.tolist()))

  st.markdown("""## Cohen's Kappa Score""")
  st.write("Cohen's Kappa Score: ",cohen_kappa_score(coder1.label.tolist(),coder2.label.tolist()))
except:
  pass
