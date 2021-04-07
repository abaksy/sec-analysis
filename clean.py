import os
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
import re
import string


def load_fileslist():
    if "fileslist.pkl" not in os.listdir("."):
        files_list = list()
        clean_files_list = list()
        for data_dir in os.listdir("./Data"):
            if data_dir.startswith("Year_"):
                for fname in os.listdir(f"Data/{data_dir}"):
                    files_list.append(f"Data/{data_dir}/{fname}")
                    clean_files_list.append(f"Clean_Data/{data_dir}/{fname}")
        filename = "fileslist.pkl"
        with open(filename, "wb") as f:
            pickle.dump(files_list, f)
        clean_filename = "cleanfileslist.pkl"
        with open(clean_filename, "wb") as f:
            pickle.dump(clean_files_list, f)
    else:
        with open("fileslist.pkl", "rb") as f:
            files_list = pickle.load(f)
        with open("cleanfileslist.pkl", "rb") as f:
            clean_files_list = pickle.load(f)
    return files_list, clean_files_list


stop = stopwords.words('english')


def stopword_remover(x): return ' '.join(
    [word for word in x.split() if word not in (stop)])


def make_clean_dir():
    os.mkdir("Clean_Data")
    for data_dir in os.listdir("./Data"):
        os.mkdir(f"Clean_Data/{data_dir}")

punkt = list(string.punctuation)

def cleanText(text: str, mode = "list"):
    stemmer = PorterStemmer()
    lem = WordNetLemmatizer()
    lowercase_text = text.lower()
    sentences = sent_tokenize(lowercase_text)
    document = list()
    doc_word_list = list()
    for sent in sentences:
        lemmas = list()
        words = word_tokenize(sent)
        for w in words:
            lem_word = lem.lemmatize(w)
            lemmas.append(lem_word)
        sentence = ' '.join(lemmas)
        document.append(sentence)
        doc_word_list += lemmas
    if mode == "string":
        clean_text = ' '.join(document)
        #print("CLEAN:", clean_text)
        clean_text = re.sub(r'[^\w\s]', '', clean_text)
        clean_text = stopword_remover(clean_text)
        return clean_text
    else:
        sw_removed_wordlist = [word for word in doc_word_list if word not in stop + punkt]
        return sw_removed_wordlist



if __name__ == "__main__":
    files_list, clean_files_list = load_fileslist()
    if "Clean_Data" not in os.listdir("."):
        make_clean_dir()
    for fname, clean_fname in zip(files_list, clean_files_list):
        print(f"Cleaning {fname}")
        with open(fname, "r") as f:
            content = f.read()
            if content != '':
                content = content.split("\n")
                title, art_id, place_date = content[:3]
                text = content[3:]
                text = '\n'.join(text)
                clean_text = cleanText(text, mode="string")
                print("Clean text of length:", len(clean_text))
                f1 = open(clean_fname, "w")
                f1.write(f"{title}\n{art_id}\n{place_date}\n{clean_text}\n")
                f1.close()
            else:
                print(f"WARNING: {fname} is empty!")
        print(f"Generated {clean_fname}")
