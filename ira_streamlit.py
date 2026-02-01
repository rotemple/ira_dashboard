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

st.set_page_config(page_title='Propaganda Data Browser')

# Set the title of the Streamlit app
st.title("📊 Data Dashboard to Browse Propaganda Data")
st.subheader('Fivethirtyeight/russian-troll-tweets. (2025). [Computer software]. FiveThirtyEight. https://github.com/fivethirtyeight/russian-troll-tweets (Original work published 2018)')

# option = st.sidebar.selectbox(
#     "Which file do you wish to browse?",
#     ('IRAhandle_tweets_1.csv','IRAhandle_tweets_2.csv','IRAhandle_tweets_3.csv',
#      'IRAhandle_tweets_4.csv','IRAhandle_tweets_5.csv','IRAhandle_tweets_6.csv',
#      'IRAhandle_tweets_7.csv','IRAhandle_tweets_8.csv','IRAhandle_tweets_9.csv',
#      'IRAhandle_tweets_10.csv','IRAhandle_tweets_11.csv','IRAhandle_tweets_12.csv',
#      'IRAhandle_tweets_13.csv',))

#st.sidebar.write('See https://github.com/rotemple/russian-troll-tweets for the complete dataset description.')
# File uploader widget in the sidebar

#url = 'https://raw.githubusercontent.com/rotemple/russian-troll-tweets/refs/heads/master/'
#df = pd.read_csv(url+option)

# df['col1'] = list(range(len(df)))
# tweets = df.content.tolist()

    
    # Display a preview of the data
# container = st.container()    
# container.subheader("Data Preview: " + option)
# container.dataframe(df)
# container.subheader("Data Preview: " + option)

# wordcloud = WordCloud().generate(' '.join(cleaned))

# plt.axis("off")

# fig = plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")


# container.pyplot(fig)
    
#     # Display basic statistics
# container.subheader("Descriptive Statistics: " + option)
# container.write(df.describe())

# st.subheader('Top-50 Hashtags for  '+option)
# try:
#     hashtags = flatten_list(flatten_list([hashtag_extract(tweet) for tweet in tweets]))
#     hcounts = pd.DataFrame(Counter(hashtags).most_common()[:50])
#     hcounts = hcounts.rename(columns={0:'hashtag',1:'count'})
    
#     st.dataframe(hcounts) 
# except:
#     st.subheader("hashtag extraction error!")

# #display top-50 mentions
# st.subheader('Top-50 Mentions for  '+option)

# try:
#     mentions =flatten_list(flatten_list([mention_extract(tweet) for tweet in tweets]))
#     counts = pd.DataFrame(Counter(mentions).most_common()[:50])
#     counts = counts.rename(columns={0:'mention',1:'count'})
    
#     st.dataframe(counts)    
# except:
#     st.subheader('mention extraction error!')


container.write('Streamlit app created by Ryan Omizo')    
