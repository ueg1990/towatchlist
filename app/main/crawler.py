import datetime

import requests
from bs4 import BeautifulSoup


TO_CRAWL = {'fullmatchesandshows':
               {'url': 'http://www.fullmatchesandshows.com/',
                'shows': {'BBC Match of the Day', 'European Football Show',
                          'ESPN FC', 'BBC Match of the Day 2'}
               },
            'watchseriesustv':
               {'url': 'http://watchseriesus.tv/',
                'shows': {'The Daily Show', ' John Oliver',
                          'Full Frontal With Samantha Bee'}
               }
           }


def crawler():
    for func, info in TO_CRAWL.items():
        yield from globals()[func](info['url'], info['shows'])


def fullmatchesandshows(url, shows):
    soup = make_soup(url)
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


def watchseriesustv(url, shows):
    today = datetime.datetime.today().date()
    soup = make_soup(url)
    divs = iter(soup.find_all('div', {'class': 'moviefilm'}))
    for div in divs:
        anchor = div.find('a', href=True)
        img = anchor.find('img')
        name = img['alt']
        for show in shows:
            if show in name:
                src = img['src']
                href = anchor['href']
                break
        else:
            continue
        yield name, href, src, today


def make_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


if __name__ == '__main__':
    for i in crawler():
        print(i)