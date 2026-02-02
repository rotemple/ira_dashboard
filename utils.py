import nltk
import pandas as pd
nltk.download('all')

import matplotlib.pyplot as plt
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer

def plot_top_words(model, feature_names, n_top_words, title):
    fig, axes = plt.subplots(2, 5, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[-n_top_words:]
        top_features = feature_names[top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx + 1}", fontdict={"fontsize": 30})
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()

def nnmf_topics(data,n_components=7,n_features=1000,n_top_words=20,batch_size=128):
  init = "nndsvda"
  print("Loading dataset...")
  
  # Use tf-idf features for NMF.
  print("Extracting tf-idf features for NMF...")
  tfidf_vectorizer = TfidfVectorizer(
      max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
  )
  
  tfidf = tfidf_vectorizer.fit_transform(data, stop_words='english')
  
  # Fit the NMF model
  print(
      "Fitting the NMF model (Frobenius norm) with tf-idf features, "
      "n_samples=%d and n_features=%d..." % (n_samples, n_features)
  )
  t0 = time()
  nmf = NMF(
      n_components=n_components,
      random_state=1,
      init=init,
      beta_loss="frobenius",
      alpha_W=0.00005,
      alpha_H=0.00005,
      l1_ratio=1,
  ).fit(tfidf)
  print("done in %0.3fs." % (time() - t0))
  
  
  tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
  plot_top_words(
      nmf, tfidf_feature_names, n_top_words, "Topics in NMF model (Frobenius norm)"
  )
  
  # Fit the NMF model
  print(
      "\n" * 2,
      "Fitting the NMF model (generalized Kullback-Leibler "
      "divergence) with tf-idf features, n_samples=%d and n_features=%d..."
      % (n_samples, n_features),
  )
  
  nmf = NMF(
      n_components=n_components,
      random_state=1,
      init=init,
      beta_loss="kullback-leibler",
      solver="mu",
      max_iter=1000,
      alpha_W=0.00005,
      alpha_H=0.00005,
      l1_ratio=0.5,
  ).fit(tfidf)
  print("done in %0.3fs." % (time() - t0))
  
  tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
  plot_top_words(
      nmf,
      tfidf_feature_names,
      n_top_words,
      "Topics in NMF model (generalized Kullback-Leibler divergence)",
  )
  


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
