# sec-analysis
Scraping and IR tasks on data from press releases put out by the US Securities and Exchange Commission

This project was done for partial fulfillment of the course requirements under the course **Algorithms for Intelligence Web and Information Retrieval** (UE18CS332)
at PES University, Bangalore


# How to run
Scrape and clean data:

```
$ git clone https://github.com/abaksy/sec-analysis
$ cd sec-analysis
$ mkdir Data
$ pip3 install -r requirements.txt
$ python3 get_data.py -s <start_year> -e <end_year>
$ python3 clean.py
```

## Tf-IDF based search engine
```
$ python3 search_engine.py
```

## LDA-Topic Model
Run the Jupyter notebook attached called sec-analysis.ipynb
