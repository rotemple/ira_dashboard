#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 14:43:46 2026

@author: tuk35906
"""

import streamlit as st
import pandas as pd

# Set the title of the Streamlit app
st.title("📊 Data Dashboard to Browse fivethirtyeights' IRA Tweet Dataset")
st.subheader('Fivethirtyeight/russian-troll-tweets. (2025). [Computer software]. FiveThirtyEight. https://github.com/fivethirtyeight/russian-troll-tweets (Original work published 2018)')



option = st.sidebar.selectbox(
    "Which file do you wish to browse?",
    ('IRAhandle_tweets_1.csv','IRAhandle_tweets_2.csv','IRAhandle_tweets_3.csv',
     'IRAhandle_tweets_4.csv','IRAhandle_tweets_5.csv','IRAhandle_tweets_6.csv',
     'IRAhandle_tweets_7.csv','IRAhandle_tweets_8.csv','IRAhandle_tweets_9.csv',
     'IRAhandle_tweets_10.csv','IRAhandle_tweets_11.csv','IRAhandle_tweets_12.csv',
     'IRAhandle_tweets_13.csv',))

st.sidebar.write('See https://github.com/rotemple/russian-troll-tweets for the complete dataset description.')
# File uploader widget in the sidebar

url = 'https://raw.githubusercontent.com/fivethirtyeight/russian-troll-tweets/refs/heads/master/'
df = pd.read_csv(url+option)
    
    # Display a preview of the data
container = st.container()    
container.subheader("Data Preview: " + option)
container.dataframe(df)
    
    # Display basic statistics
container.subheader("Descriptive Statistics: " + option)
container.write(df.describe())
    
