import requests
from bs4 import BeautifulSoup
import os


class SEC_Base:
    def __init__(self):
        '''
        Base class for all SEC scraping operations
        '''
        self.base_url = "https://www.sec.gov"
        self.pr_url = "https://www.sec.gov/news/pressreleases"

    def get_url_all(self, year):
        '''
        Return the URL for the page containing the list of all links
        for a given year
        '''
        return self.pr_url + f"?aId=edit-year&year={year}&month=All&items_per_page=100&page=2&items_per_page=All"


class Article:
    def __init__(self, url, article_id, title, text, date_location):
        self.url = url
        self.article_id = article_id
        self.title = title
        self.text = ''
        self.dateloc = date_location

    def __str__(self) -> str:
        return f"Article({self.article_id}, {self.dateloc})"


class SEC_LinkScraper(SEC_Base):
    def __init__(self, year):
        '''
        Scrapes links to SEC press releases for a single year
        '''
        super(SEC_LinkScraper, self).__init__()
        self.year = year
        self.links = []
        self.num_links = 0
        self.articles = []

    def scrape_links(self):
        '''
        Return complete URLs
        to all articles for a given year
        '''
        url = self.get_url_all(self.year)
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")
        self.links = [self.base_url + i.attrs["href"] for i in links if "href" in i.attrs.keys() and (
            "/news/pressrelease/" in i.attrs["href"] or "/news/press-release" in i.attrs["href"])]
        print(f"GOT LINKS FOR {len(self.links)} ARTICLES IN YEAR {self.year}")
        # return self.links

    def scrape_articles(self):
        '''
        Get text for each article
        '''
        ctr = 0
        dir_name = f"Data/Year_{self.year}"
        os.mkdir(dir_name)
        for url in self.links:
            print(f"Scraping article {ctr+1} in year {self.year}")
            ctr += 1
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            at1 = [i.text for i in soup.find(
                'div', {'class': 'article-body'}).find_all('p')]
            at2 = [i.text for i in soup.find(
                'div', {'class': 'article-body'}).find_all('div')]
            if at1 == []:
                articletext = ' '.join(at2).strip('\n').strip('\t')
            else:
                articletext = ' '.join(at1).strip('\n').strip('\t')
            art_id = url.split('/')[-1].split(".")[0]
            title = soup.find_all('title')[0].text
            dateloc = soup.find_all(
                'p', {'class': 'article-location-publishdate'})[0].text.strip()
            at = Article(url, art_id, title, articletext, dateloc)
            self.articles.append(at)

            file = open(f"{dir_name}/{art_id}.txt", 'w', encoding="utf-8")
            file.write(title+'\n')
            file.write(art_id+'\n')
            file.write(dateloc+'\n')
            file.write(articletext)
            file.close()

        print(f"GOT {len(self.articles)} ARTICLES IN YEAR {self.year}")
        # return self.articles
