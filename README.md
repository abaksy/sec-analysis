# sec-analysis
Scraping and IR tasks on data from press releases put out by the US Securities and Exchange Commission

This project was done for partial fulfillment of the course requirements under the course **Algorithms for Intelligence Web and Information Retrieval** (UE18CS332)
at PES University, Bangalore


# How to run
Scrape and clean data:

```
$ git clone https://github.com/abaksy/sec-analysis
$ cd sec-analysis
$ pip3 install -r requirements.txt
$ python3 src/get_data.py -s <start_year> -e <end_year>
$ python3 src/clean.py
```

## Tf-IDF based search engine
```
$ python3 src/search_engine.py
```

## LDA-Topic Model
Run the Jupyter notebook attached called notebooks/sec-analysis.ipynb
