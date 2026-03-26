#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 14:43:46 2026

@author: Ryan Omizo
"""
import streamlit as st
import pandas as pd
import re
import itertools
from collections import Counter
from wordcloud import WordCloud
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize

nltk.download('all')

  
stops = set(stopwords.words('english'))
wn = WordNetLemmatizer()
def preprocess(text):
  tokens = nltk.wordpunct_tokenize(text) #tokenize text
  filtered_tokens = [token.lower() for token in tokens if token.lower() not in stops and not re.search('\d',token)] #remove stopwords
  lemmas = [wn.lemmatize(ft) for ft in filtered_tokens] #convert tokens to lemmas
  final_lemmas = [lemma for lemma in lemmas if len(lemma) > 4] #remove tokens < length 1.
  return final_lemmas

def flatten_list(somelist):
        if any(isinstance(el, list) for el in somelist) == False:
            return somelist
        flat_list = list(itertools.chain(*somelist))
        return flat_list

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
@st.cache_data
def load_csv(url):
  df = pd.read_csv(url)
  return df

# Set the title of the Streamlit app
st.title("📊 Data Dashboard to Browse YouTube Comemnts to the Trump/Vance Disinformation Campaign Against Haitian Communities in Springfield, OH")
st.subheader('Omizo, R. M. (2025). Disinformation on Youtube: A Dataset of Youtube Comments on Videos Related to Claims Made by Trump and Vance on Haitian Immigrants. Journal of Open Humanities Data, 11, 12. https://doi.org/10.5334/johd.283')
st.sidebar.write('See https://doi.org/10.5334/johd.283 for the complete dataset description.')
# File uploader widget in the sidebar

url = 'https://raw.githubusercontent.com/rotemple/ira_dashboard/refs/heads/main/pages/youtube_haitian_disinformation_comment_reply_metadata.csv'
df = load_csv(url)

container = st.container()
container.markdown("""## Data Preview: YouTube Video Information""")
vdf = load_csv('https://raw.githubusercontent.com/rotemple/ira_dashboard/refs/heads/main/pages/youtube_haitian_disinformation_video_meta.csv')
container.dataframe(vdf)
container.markdown("""## Data Preview: YouTube Comments""")
container.dataframe(df)

container.markdown("""## Comments by Video Id""")
video_select = container.multiselect(label='filter by video id',options=vdf.video_id.unique().tolist())

dfs = []
for video in video_select:
  d = vdf[vdf['video_id'] == video]
  comments = flatten_list(d['comments'].tolist())
  fd = pd.DataFrame()
  fd['video_id'] = [video_id] * len(comments)
  fd['comment'] = comments
  dfs.append(fd)

fds = pd.concat(dfs)
container.dataframe(fds)

container.write('Streamlit app created by Ryan Omizo')    
