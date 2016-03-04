import json

import requests
from bs4 import BeautifulSoup


TO_CRAWL = {'http://www.fullmatchesandshows.com/': ['BBC Match of the Day',
            'European Football Show', 'ESPN FC']}


def crawl():
    for website, shows in TO_CRAWL.items():
        response = requests.get(website)
        soup = BeautifulSoup(response.text, 'html.parser')


if __name__ == '__main__':
    crawl()