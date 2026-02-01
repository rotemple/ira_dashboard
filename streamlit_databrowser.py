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

st.set_page_config(page_title='Political Communication Data Browser')

# Set the title of the Streamlit app
st.title("📊 Political Communication Data Browser")
#st.subheader('Fivethirtyeight/russian-troll-tweets. (2025). [Computer software]. FiveThirtyEight. https://github.com/fivethirtyeight/russian-troll-tweets (Original work published 2018)')

    # Display a preview of the data
container = st.container()    
container.write('Select an option from the sidebar to browse a corpus of political and/or social media communications')


container.write('Streamlit app created by Ryan Omizo')    
