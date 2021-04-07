import pickle
from gensim import models
from gensim.corpora import Dictionary
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from clean import stopword_remover, cleanText
import numpy as np


f = open("cleanfileslist.pkl", "rb")
cleanfileslist = pickle.load(f)
mapping = Dictionary()

documents = list()
lem = WordNetLemmatizer()
for fname in cleanfileslist:
    try:
        with open(fname, "r") as f:
            print(fname)
            content = f.read()
            content = content.split("\n")
            title, art_id, place_date = content[:3]
            text = ''.join(content[3:])
            doc = cleanText(text, mode="string")
            sents = sent_tokenize(doc)
            document = list()
            for sent in sents:
                lem_words = list()
                words = word_tokenize(sent)
                for w in words:
                    lem_word = lem.lemmatize(w)
                    lem_words.append(lem_word)
                document += lem_words
            documents.append(document)
    except Exception as e:
        print(e)
        continue

BoW_corpus = [mapping.doc2bow(doc, allow_update=True) for doc in documents]
tfidf = models.TfidfModel(BoW_corpus, smartirs='ntc')
tfidf_corpus = tfidf[BoW_corpus]

lda_model_tfidf = models.LdaMulticore(tfidf_corpus, num_topics=50, id2word=mapping, passes=2, workers=4)
lda_model_tfidf.save("lda.model")
