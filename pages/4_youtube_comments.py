#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 14:43:46 2026

@author: tuk35906
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
        

# Set the title of the Streamlit app
st.title("📊 Data Dashboard to Browse YouTube Comemnts to the Trump/Vance Disinformation Campaign Against Haitian Communities in Springfield, OH")
st.subheader('Omizo, R. M. (2025). Disinformation on Youtube: A Dataset of Youtube Comments on Videos Related to Claims Made by Trump and Vance on Haitian Immigrants. Journal of Open Humanities Data, 11, 12. https://doi.org/10.5334/johd.283')
st.sidebar.write('See https://doi.org/10.5334/johd.283 for the complete dataset description.')
# File uploader widget in the sidebar

url = 'https://raw.githubusercontent.com/rotemple/ira_dashboard/refs/heads/main/pages/youtube_haitian_disinformation_comment_reply_metadata.csv'
df = pd.read_csv(url)

comments = df.comment.tolist()

    
    # Display a preview of the data
container = st.container()    
container.subheader("Data Preview")
container.dataframe(df)

cleaned = [preprocess(comment) for comment in comments]
wordcloud = WordCloud().generate(' '.join(cleaned))

plt.axis("off")

fig = plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")


container.pyplot(fig)
    
    # Display basic statistics
container.subheader("Descriptive Statistics")
container.write(df.describe())




container.write('Streamlit app created by Ryan Omizo')    
