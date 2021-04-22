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

# Construct vocabulary for TF-IDF
df = pd.read_csv("textclean.csv")
docs = list(df["Keyword_final"])
vocab = set()
for text in docs:
    vocab.update(text.split(","))

# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer(vocabulary=vocab)

# It fits the data and transform it as a vector
X = vectorizer.fit_transform(docs)

# Convert the X as transposed matrix
X = X.T.toarray()
vect_df = pd.DataFrame(X, index=vectorizer.get_feature_names())


def get_similar_articles(q, df):
    print("Query:", q)
    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
    print("Query vector:", q_vec)
    sim = {}  # Calculate the similarity
    for i in range(10):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / \
            np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    for k, v in sim_sorted:
        if v != 0.0:
            print("Similarity:", v)
            print(docs[k])
            print()


query = input("Enter search query:")

get_similar_articles(query, vect_df)
