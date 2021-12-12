import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Construct vocabulary for TF-IDF
df = pd.read_csv("../data/textclean.csv")
docs = list(df["Keyword_final"])
art_ids = list(df["Article_ID"])
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


def display_articles(article_ids, query):
    df1 = pd.read_csv("Clean_Data.csv")
    raw_texts = list()
    print("RESULTS:")
    for ele in article_ids:
        sim_value, art_id = ele
        df_joined = df.merge(df1, on="Article_ID")
        raw_text = df_joined.loc[df_joined.Article_ID ==
                                 art_id]["Raw_Text"].values[0]
        print(f"Similarity: {sim_value}")
        print(f"Article ID: {art_id}")
        raw_texts.append((art_id, raw_text))
    print("Length of raW_text list is", len(raw_texts))
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(f"QUERY: {query}\n\n")
        for item in raw_texts:
            print(f"WRITING {item[0]} to file")
            raw_text = item[1].encode("utf-8").decode()
            print(raw_text)
            f.write(f"ARTICLE ID: {item[0]}\n{raw_text}\n\n")

def clean_query(query):
    lem = WordNetLemmatizer()
    query = word_tokenize(query)
    clean_query = list()
    for word in query:
        clean_query.append(lem.lemmatize(word))
    return clean_query

def get_similar_articles(query, df):
    #print("Query:", query)
    query = clean_query(query)
    print(query)
    similar_articles = list()
    q_vec = vectorizer.transform(query).toarray().reshape(df.shape[0],)
    #print("Query vector:", q_vec)
    sim = {}  # Calculate the similarity
    for i in range(10):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / \
            np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    for k, v in sim_sorted:
        if v != 0.0:
            similar_articles.append((v, art_ids[k]))
    display_articles(similar_articles, query)


query = input("Enter search query:")

get_similar_articles(query, vect_df)
