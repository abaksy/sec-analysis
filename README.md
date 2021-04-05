# sec-analysis
Scraping and IR tasks on data from press releases put out by the US Securities and Exchange Commission

This project was done for partial fulfillment of the course requirements under the course **Algorithms for Intelligence Web and Information Retrieval** (UE18CS332)
at PES University, Bangalore

## Cleaning

* Convert to lowercase
* Remove stopwords
* Sentence tokenization
* Get n-grams from each sentence

# How to run

```
$ git clone https://github.com/abaksy/sec-analysis
$ cd sec-analysis
$ mkdir Data
$ pip3 install -r requirements.txt
$ python3 get_data.py -s <start_year> -e <end_year>
$ python3 clean.py
```
