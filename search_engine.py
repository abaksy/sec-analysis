import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords

from gensim import models
from gensim.corpora import Dictionary

import re
import string
import sys
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

import warnings
warnings.filterwarnings("ignore")



df = pd.read_csv("Clean_Data.csv")

docs = list()

for _, row in df.iterrows():
    text = row["Text"]
    docs.append(text)




# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer()

# It fits the data and transform it as a vector
X = vectorizer.fit_transform(docs)

# Convert the X as transposed matrix
X = X.T.toarray()

vect_df = pd.DataFrame(X, index=vectorizer.get_feature_names())

print("Vect_df created")
print(vect_df)



def get_similar_articles(q, df):
  print("query:", q)
#   print("Berikut artikel dengan nilai cosine similarity tertinggi: ")  # Convert the query become a vector
  q = [q]
  q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
  sim = {}  # Calculate the similarity
  for i in range(10):
    sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
  # Sort the values 
  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)  # Print the articles and their similarity values
  for k, v in sim_sorted:
    if v != 0.0:
      print("Similaritas:", v)
      print(docs[k])
      print()


query = "fraud government"

get_similar_articles(query, vect_df)