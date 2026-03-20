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
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import gutenberg
from nltk.text import Text

@st.cache_data
def nltk_download():
  nltk.download('all')

@st.cache_data
def get_stops():
  stops = set(stopwords.words('english'))
  return stops

@st.cache_data
def get_lemmatizer():
  return WordNetLemmatizer()

nltk_download()
stops = get_stops()
wn = get_lemmatizer()

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
def mention_extract(x):
    mentions = []
    # Loop over the words in the tweet
    for i in x.split():
        ht = re.findall(r"(@\w+)", i)
        if ht == []:
            pass
        else:
            mentions.append(ht)

    return mentions
@st.cache_data
def hashtag_extract(x):
    hashtags = []
    # Loop over the words in the tweet
    for i in x.split():
        ht = re.findall(r"(#\w+)", i)
        if ht == []:
            pass
        else:
            hashtags.append(ht)

    return hashtags

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def search_dataframe(dataframe,query):
    dataframe['text'] = dataframe.text.str.lower()
    dataframe['search'] = dataframe.text.str.contains(query)
    return dataframe[dataframe['search'] == True]

st.set_page_config(page_title='Hannah (2022) QAnon Tweet Dataset')

# Set the title of the Streamlit app
st.title("📊 Data Dashboard to Browse Hannah's (2022) QAnon Tweet Dataset")
st.subheader('Hannah, M. N. (2022). Collection of tweets related to QAnon hashtags. Purdue University Research Repository. doi:10.4231/32MD-DB04')
st.write('For the dataset description, see https://purr.purdue.edu/publications/4171/about/1#citethis')


# File uploader widget in the sidebar
base_url = 'https://raw.githubusercontent.com/rotemple/ira_dashboard/refs/heads/main/pages/'
filenames = ['qanon_tweets_0.csv',
             'qanon_tweets_1.csv',
             'qanon_tweets_2.csv',
             'qanon_tweets_3.csv',
             'qanon_tweets_4.csv',
             'qanon_tweets_5.csv',
             # 'qanon_tweets_6.csv',
             # 'qanon_tweets_7.csv',
             # 'qanon_tweets_8.csv',
             # 'qanon_tweets_9.csv',
             # 'qanon_tweets_10.csv',
            #  'qanon_tweets_11.csv',
            #  'qanon_tweets_12.csv',
            #  'qanon_tweets_13.csv',
            #  'qanon_tweets_14.csv',
            #  'qanon_tweets_15.csv',
            #  'qanon_tweets_16.csv',
            #  'qanon_tweets_17.csv',
            #  'qanon_tweets_18.csv',
            #  'qanon_tweets_19.csv',
            #  'qanon_tweets_20.csv',
            #  'qanon_tweets_21.csv',
            #  'qanon_tweets_22.csv',
            #  'qanon_tweets_23.csv',
            #  'qanon_tweets_24.csv',
            # 'qanon_tweets_25.csv',
            ]
@st.cache_data
def load_csv(url):
  return pd.read_csv(url)
  
dfs = [load_csv(base_url+f) for f in filenames]
df = pd.concat(dfs)
df['col1'] = list(range(len(df)))

    
    # Display a preview of the data
container = st.container()    
container.subheader("Data Preview")
container.dataframe(df)

#get hashtags
tweets = df.dropna(subset='text').text.tolist()

 # Display basic statistics
container.subheader("Descriptive Statistics")
container.write(df.describe())

try:
  hashtags = flatten_list(flatten_list([hashtag_extract(tweet) for tweet in tweets]))
  hcounts = pd.DataFrame(Counter(hashtags).most_common()[:50])
  hcounts = hcounts.rename(columns={0:'hashtag',1:'count'})
  st.subheader('Top-50 Hashtags')
  st.dataframe(hcounts) 
except:
  st.subheader("hashtag extraction error!")
  
  #get metions
st.subheader('Top-50 Mentions')

try:
  mentions =flatten_list(flatten_list([mention_extract(tweet) for tweet in tweets]))
  counts = pd.DataFrame(Counter(mentions).most_common()[:50])
  counts = counts.rename(columns={0:'mention',1:'count'})
    
  st.dataframe(counts)    
except:
  st.subheader('mention extraction error!')

csv = convert_df(df)
st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)  
# Basic Search
keyword = st.sidebar.text_input(label='Basic Search')
st.dataframe(search_dataframe(df, keyword))
# Concordancer

query = st.sidebar.text_input(label='Search the corpus for keywords in context')

@st.cache_data
def make_corpus(content):
  return Text(nltk.word_tokenize(str(content).lower()))
  
corpus = make_corpus(tweets)
corpus_concordance = corpus.concordance_list(query.lower(),width=150,lines=len(tweets))
cf = pd.DataFrame({'text':[c.line for c in corpus_concordance]})
st.subheader('Concordance Search Results')
st.dataframe(cf)

   


container.write('Streamlit app created by Ryan Omizo')    
