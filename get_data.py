import scraper
import pandas as pd
import argparse
from sys import exit

p = argparse.ArgumentParser()
p.add_argument("-s", "--start", help="Start year for scraping", type=int)
p.add_argument("-e", "--end", help="End year for scraping", type=int)
args = p.parse_args()

s, e = args.start, args.end

if s >= e:
    print("Start year cannot be greater than or equal to end year!")
    exit(-1)

years = list(range(s, e+1))
'''
For each year create a scraper.SEC_LinkScraper(year) object

For each object call the scrape_links() and scrape_articles() methods (in this order)

Now we need to figure out a way in which we are actually gonna store the data that is there in
each of these object in the form of files on disk

Single File for all articles? One file for each year? Each article gets its own separate file?
'''
