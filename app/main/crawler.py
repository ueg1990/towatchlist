import datetime

import requests
from bs4 import BeautifulSoup


TO_CRAWL = {'fullmatchesandshows':
               {'url': 'http://www.fullmatchesandshows.com/',
                'shows': ['BBC Match of the Day', 'European Football Show',
                          'ESPN FC']
               }
            }


def crawl():
    for crawler, info in TO_CRAWL.items():
         yield from globals()[crawler](info)


def fullmatchesandshows(info):
    url = info['url']
    shows = info['shows']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = iter(soup.find_all('div', {'class': 'td-block-span4'}))
    for div in divs:
        entry = div.find(itemprop='url')
        name = entry['title']
        if name.split(chr(8211))[0].strip() in shows:
            href = entry['href']
            image = div.find(itemprop='image')['src']
            image = image.split('?')[0]
            date = div.find(itemprop='dateCreated')['datetime'].split('T')[0]
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            yield name, href, image, date


if __name__ == '__main__':
    for i in crawl():
        print(i)