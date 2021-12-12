import scraper
import argparse
from sys import exit

p = argparse.ArgumentParser()
p.add_argument("-s", "--start", help="Start year for scraping", type=int)
p.add_argument("-e", "--end", help="End year for scraping", type=int)
args = p.parse_args()

s, e = args.start, args.end

if s is None or e is None:
    print("Usage: \npython3 get_data.py --start <year> --end <year> \n python3 get_data.py -s <year> -e <year>")
    exit(-1)

if s >= e:
    print("Error: Start year cannot be greater than or equal to end year!")
    exit(-1)

years = list(range(s, e+1))
'''
For each year create a scraper.SEC_LinkScraper(year) object

For each object call the scrape_links() and scrape_articles() methods (in this order)
'''
for year in years:
    year_scraper = scraper.SEC_LinkScraper(year)
    year_scraper.scrape_links()
    year_scraper.scrape_articles()
