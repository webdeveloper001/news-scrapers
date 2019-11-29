# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewsthehindu(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


    url = 'https://www.thehindu.com/search/?q=' + keyword

    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    pagecount = 1
    for pagelink in soup.findAll('a', class_='page-link'):
        if pagecount < int(pagelink.attrs['data-page-no']):
            pagecount = int(pagelink.attrs['data-page-no'])
    print(pagecount)
    for page in range(1, pagecount + 1):
        print(page)
        url = 'https://www.thehindu.com/search/?q={}%5C&order=DESC&sort=publishdate&page={}'
        r = session.get(url.format(keyword, page))
        soup = BeautifulSoup(r.text, features="html.parser")
        news_list = soup.findAll('div', class_='75_1x_StoryCard')
        for news in news_list:
            classifier = news.find('a', class_='section-name').text
            title = news.find('a', class_='story-card75x1-text').text.strip()
            url = news.find('a', class_='story-card75x1-text').attrs['href']
            date = datetime.datetime.strptime(soup.find('span', class_='dateline').text, ' %B %d, %Y')
            year = date.year
            month = date.month
            day = date.day
            summary = news.find('span', class_='story-card-33-text').text
            data.append((title, url, summary, (year, month, day), classifier, 'thehindu'))
            print(title, url, summary, (year, month, day), classifier, 'thehindu')
    return data
extractNewsthehindu('indo')