import pandas as pd
import os
import re
import nltk
import pickle
import string

from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
from nltk.corpus import wordnet as wn


def load_fileslist(dirname):
    '''
    Input: A directory containing SEC articles
    Output: A list of filepaths for the original data

    Saves the two files lists into pickle files to be loaded later
    If pickle files already exist then just open instead of creating new pickle files
    '''
    if "fileslist.pkl" not in os.listdir("."):
        files_list = list()
        clean_files_list = list()
        for data_dir in os.listdir(f"./{dirname}"):
            if data_dir.startswith("Year_"):
                for fname in os.listdir(f"{dirname}/{data_dir}"):
                    files_list.append(f"{dirname}/{data_dir}/{fname}")
                    clean_files_list.append(
                        f"Clean_{dirname}/{data_dir}/{fname}")
        filename = f"fileslist_{dirname}.pkl"
        with open(filename, "wb") as f:
            pickle.dump(files_list, f)
    else:
        with open(f"fileslist_{dirname}.pkl", "rb") as f:
            files_list = pickle.load(f)
    return files_list


def stopword_remover(x): return ' '.join(
    [word for word in x.split() if word not in (stopwords.words('english'))])


def cleanText(text: str):
    '''
    Input: Uncleaned text as string
    Output: Cleaned text as string
    '''
    # Remove URL
    url_remove = re.sub(
        r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", '', text)
    lem = WordNetLemmatizer()
    stop = stopwords.words('english')
    punkt = list(string.punctuation)
    sentences = sent_tokenize(text)
    document = list()
    doc_word_list = list()
    for sent in sentences:
        lemmas = list()
        # Text -> List of words
        words = word_tokenize(sent)
        pos_tags = pos_tag(words)
        word_new = list()
        for tag in pos_tags:
            if tag[1] not in ["NNP", "NNPS"]:
                # List of words -> List of words without proper nouns
                word_new.append(tag[0])
        for w in word_new:
            # List of words -> List of lemmas
            lem_word = lem.lemmatize(w)
            lemmas.append(lem_word)
        # List of lemmas -> Sentence
        sentence = ' '.join(lemmas)
        # Sentence -> List of sentences
        document.append(sentence)
    # List of sentences -> Text string
    clean_text = ' '.join(document)
    # To lower case
    clean_text = clean_text.lower()
    clean_text = re.sub(r'[^\w\s]', '', clean_text)
    clean_text = stopword_remover(clean_text)
    return clean_text


def get_clean_data_df():
    '''
    Reads uncleaned data that was scraped, cleans it and returns a dataframe
    '''
    df = pd.DataFrame(columns=["Title", "Article_ID",
                      "Date_Place", "Raw_Text", "Text", "Clean_Text"])
    files_list = load_fileslist("Data")
    lem = WordNetLemmatizer()
    counter = 0
    for fname in files_list:
        #print(f"Cleaning {fname}")
        with open(fname, "r", encoding="utf-8") as f:
            content = f.read()
        if content != '':
            content = content.split("\n")
            title, art_id, place_date = content[:3]
            text = content[3:]
            text = '\n'.join(text)
            clean_text = cleanText(text)
            sents = sent_tokenize(clean_text)
            document = list()
            for sent in sents:
                lem_words = list()
                words = word_tokenize(sent)
                for w in words:
                    lem_word = lem.lemmatize(w)
                    lem_words.append(lem_word)
                document += lem_words
            row = {"Title": title, "Article_ID": art_id, "Date_Place": place_date,
                   "Raw_Text": text, "Text": clean_text, "Clean_Text": str(document)}
            df = df.append(row, ignore_index=True)
            counter += 1
        else:
            pass
    print(f"Generated {counter} cleaned files")
    return df


def label_clean_data(df):
    labels = []
    fraud_words = set(
        ["fraud", "whistleblower", "complaint", "disclosure", "charge"])

    for _, row in df.iterrows():
        title = row["Title"]
        text = set(eval(row["Clean_Text"]))
        if "fraud" in title.lower() and text.intersection(fraud_words) != set():
            labels.append(1)
        else:
            labels.append(0)
    df.insert(len(df.columns), "Fraud", labels, True)
    return df

# WordNetLemmatizer requires Pos tags to understand if the word is noun or verb or adjective etc. By default it is set to Noun


def tfidf_cleaner(data, art_ids):
    '''
    Build dataframe needed for TF-IDF Search engine
    '''
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    clean_df = pd.DataFrame()
    word_Lemmatized = WordNetLemmatizer()
    for index, d in enumerate(zip(data, art_ids)):
        entry = d[0]
        art_id = d[1]
        print(f"Processing row {index}")
        #print(index, entry)
        # Declaring Empty List to store the words that follow the rules for this step
        Final_words = []
        # Initializing WordNetLemmatizer()
        # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
        for word, tag in pos_tag(entry):
            #print(word, tag)
            # Below condition is to check for Stop words and consider only alphabets
            if len(word) > 1 and word not in stopwords.words('english') and word.isalpha():
                word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
                Final_words.append(word_Final)
            # The final processed set of words for each iteration will be stored in 'text_final'
                clean_df.loc[index, 'Keyword_final'] = str(Final_words)
                clean_df.loc[index, 'Keyword_final'] = str(Final_words)
                clean_df = clean_df.replace(
                    to_replace="\[.", value='', regex=True)
                clean_df = clean_df.replace(
                    to_replace="'", value='', regex=True)
                clean_df = clean_df.replace(
                    to_replace=" ", value='', regex=True)
                clean_df = clean_df.replace(
                    to_replace='\]', value='', regex=True)
        clean_df.loc[index, "Article_ID"] = art_id
    return clean_df


df1 = get_clean_data_df()
df1 = label_clean_data(df1)
df1.to_csv("Clean_Data.csv", index=False)

clean_texts = df1["Clean_Text"]
art_ids = list(df1["Article_ID"])
clean_texts = [eval(x) for x in clean_texts]

output = tfidf_cleaner(clean_texts, art_ids)
output.to_csv("textclean.csv", index=False)
