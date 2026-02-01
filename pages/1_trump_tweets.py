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
st.set_page_config(
  page_title="Trump Tweets",
  )

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
# Set the title of the Streamlit app
st.title("📊 Data Dashboard to Browse Trump Tweets")
st.subheader('Tweets from Trump Twitter Archive')
st.write('Brown, B. (n.d.). Search on Trump Twitter Archive. Retrieved February 1, 2026, from //www.thetrumparchive.com')



st.sidebar.write('See https://github.com/rotemple/russian-troll-tweets for the complete dataset description.')
# File uploader widget in the sidebar

df = pd.read_csv('tweets_01-08-2021.csv',on_bad_lines='skip')

df['col1'] = list(range(len(df)))
tweets = df.text.tolist()

    
    # Display a preview of the data
container = st.container()    
container.subheader("Data Preview")
container.dataframe(df)

wordcloud = WordCloud().generate(' '.join(cleaned))

plt.axis("off")

fig = plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")


container.pyplot(fig)
