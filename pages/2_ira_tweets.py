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
# import nltk
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# from nltk.tokenize import wordpunct_tokenize
# from nltk.corpus import gutenberg
# from nltk.text import Text

# @st.cache_data
# def nltk_download():
#   nltk.download('all')

# nltk_download()

# stops = set(stopwords.words('english'))
# wn = WordNetLemmatizer()
# def preprocess(text):
#   tokens = nltk.wordpunct_tokenize(text) #tokenize text
#   filtered_tokens = [token.lower() for token in tokens if token.lower() not in stops and not re.search('\d',token)] #remove stopwords
#   lemmas = [wn.lemmatize(ft) for ft in filtered_tokens] #convert tokens to lemmas
#   final_lemmas = [lemma for lemma in lemmas if len(lemma) > 4] #remove tokens < length 1.
#   return final_lemmas

def flatten_list(somelist):
        if any(isinstance(el, list) for el in somelist) == False:
            return somelist
        flat_list = list(itertools.chain(*somelist))
        return flat_list

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
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


def search_dataframe(dataframe,query):
    dataframe['content'] = dataframe.content.str.lower()
    dataframe['search'] = dataframe.content.str.contains(query)
    return dataframe[dataframe['search'] == True]

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
  
# Set the title of the Streamlit app
st.title("📊 Data Dashboard to Browse fivethirtyeights' IRA Tweet Dataset")
st.subheader('Fivethirtyeight/russian-troll-tweets. (2025). [Computer software]. FiveThirtyEight. https://github.com/fivethirtyeight/russian-troll-tweets (Original work published 2018)')
st.write('See https://github.com/rotemple/russian-troll-tweets for the complete dataset description.')

option = st.sidebar.selectbox(
    "Which file do you wish to browse?",
    ('IRAhandle_tweets_1.csv','IRAhandle_tweets_2.csv','IRAhandle_tweets_3.csv',
     'IRAhandle_tweets_4.csv','IRAhandle_tweets_5.csv','IRAhandle_tweets_6.csv',
     'IRAhandle_tweets_7.csv','IRAhandle_tweets_8.csv','IRAhandle_tweets_9.csv',
     'IRAhandle_tweets_10.csv','IRAhandle_tweets_11.csv','IRAhandle_tweets_12.csv',
     'IRAhandle_tweets_13.csv',))

# File uploader widget in the sidebar

  
url = 'https://raw.githubusercontent.com/rotemple/russian-troll-tweets/refs/heads/master/'

@st.cache_data
def load_csv(url):
  return pd.read_csv(url,usecols=['author','content','following','followers','account_type','account_category'])
  
df = load_csv(url+option)
df_content = df.content.tolist()


#df['col1'] = list(range(len(df)))

    
    # Display a preview of the data
container = st.container()    
container.subheader("Data Preview: " + option)
troll_select = container.selectbox('Filter by Troll Type:',['None'] + df.account_type.unique().tolist())
category_select = container.selectbox('Filter by Troll Category:',['None'] + df.account_category.unique().tolist())
filtered_authors = container.multiselect(label='filter by author',options=df.author.unique().tolist())

dfs = []
for author in filtered_authors:
  d = df[df['author'] == author]
  dfs.append(d)

if len(dfs) > 0:
  df = pd.concat(dfs)
else:
  pass
if troll_select == "None" and category_select == 'None':
  container.dataframe(df)
  

#get hashtags
  tweets = df.content.tolist()
  try:
    hashtags = flatten_list(flatten_list([hashtag_extract(tweet) for tweet in tweets]))
    hcounts = pd.DataFrame(Counter(hashtags).most_common()[:50])
    hcounts = hcounts.rename(columns={0:'hashtag',1:'count'})
    st.subheader('Top-50 Hashtags for '+option)
    st.dataframe(hcounts) 
  except:
    st.subheader("hashtag extraction error!")
  
  #get metions
  st.subheader('Top-50 Mentions for '+option)
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
    
elif troll_select == 'None':
  df = df[df['account_category'] == category_select]
  container.dataframe(df)
  
  #get hashtags
  tweets = df.content.tolist()
  try:
    hashtags = flatten_list(flatten_list([hashtag_extract(tweet) for tweet in tweets]))
    hcounts = pd.DataFrame(Counter(hashtags).most_common()[:50])
    hcounts = hcounts.rename(columns={0:'hashtag',1:'count'})
    st.subheader('Top-50 Hashtags for ' + category_select + ' '+option)
    st.dataframe(hcounts) 
  except:
    st.subheader("hashtag extraction error!")
  
  #get metions
  st.subheader('Top-50 Mentions for ' + category_select + ' '+option)
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

elif category_select == 'None':
  df = df[df['account_type'] == troll_select]
  container.dataframe(df)
  
  #get hashtags
  tweets = df.content.tolist()
  try:
    hashtags = flatten_list(flatten_list([hashtag_extract(tweet) for tweet in tweets]))
    hcounts = pd.DataFrame(Counter(hashtags).most_common()[:50])
    hcounts = hcounts.rename(columns={0:'hashtag',1:'count'})
  except:
    st.subheader("hashtag extraction error!")
  st.subheader('Top-50 Hashtags for ' + troll_select + ' ' +option)
  st.dataframe(hcounts) 
  #get metions
  st.subheader('Top-50 Mentions for ' +troll_select + ' '+option)
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

else:
  d = df[df['account_type'] == troll_select]
  container.dataframe(d[d['account_category'] == category_select])
  
  #get hashtags
  tweets = d.content.tolist()
  try:
    hashtags = flatten_list(flatten_list([hashtag_extract(tweet) for tweet in tweets]))
    hcounts = pd.DataFrame(Counter(hashtags).most_common()[:50])
    hcounts = hcounts.rename(columns={0:'hashtag',1:'count'})
    
    st.subheader('Top-50 Hashtags for ' + troll_select + ' & ' + category_select + ' ' +option)
    st.dataframe(hcounts) 
  except:
    st.subheader("hashtag extraction error!")
    
  
  #get metions
  st.subheader('Top-50 Hashtags for ' + troll_select + ' & ' + category_select + ' ' +option)
  try:
    mentions =flatten_list(flatten_list([mention_extract(tweet) for tweet in tweets]))
    counts = pd.DataFrame(Counter(mentions).most_common()[:50])
    counts = counts.rename(columns={0:'mention',1:'count'})
    
    st.dataframe(counts)    
  except:
    st.subheader('mention extraction error!')
  csv = convert_df(d)
  st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
# Basic Search
st.subheader('Keyword Search Results')
keyword = st.sidebar.text_input(label='Basic Search')
searched_df = search_dataframe(df,keyword)
#st.write(searched_df.describe())
st.dataframe(searched_df)

# Create Sample Dataset 
st.subheader("Create Sampled Dataset")
fraction = st.number_input('Enter sample size (e.g., .10 or .25)', min_value=.10)

dataset_button = st.button('Click to sample the dataset')
if fraction and dataset_button:
  st.write('Note: samples will be based on account names')
  gf = pd.DataFrame(df.groupby('author').sample(frac=fraction))
  g_csv = convert_df(gf)
  st.download_button(
     "Press to Download Sampled Dataset",
     g_csv,
     "sampled_dataset.csv",
     "text/csv",
     key='download-sampled-csv'
  )

# Concordancer
# query = st.sidebar.text_input(label='Search the corpus for keywords in context')

# @st.cache_data
# def make_corpus(content):
#   return Text(nltk.word_tokenize(str(content).lower()))
  
# corpus = make_corpus(df_content)

# corpus_concordance = corpus.concordance_list(query.lower(),width=150,lines=len(df_content))
# cf = pd.DataFrame({'text':[c.line for c in corpus_concordance]})
# st.subheader('Concordance Search Results')
# st.dataframe(cf)

    # Display basic statistics
# container.subheader("Descriptive Statistics: " + option)
# container.write(df.describe())

# st.subheader('Top-50 Hashtags for  '+option)
# st.dataframe(hcounts) 


#display top-50 mentions
# st.subheader('Top-50 Mentions for  '+option)

# try:
#     mentions =flatten_list(flatten_list([mention_extract(tweet) for tweet in tweets]))
#     counts = pd.DataFrame(Counter(mentions).most_common()[:50])
#     counts = counts.rename(columns={0:'mention',1:'count'})
    
#     st.dataframe(counts)    
# except:
#     st.subheader('mention extraction error!')


st.sidebar.write('Streamlit app created by Ryan Omizo')    
