# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewspulseitmagazine(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })
    page = 0
    while page >= 0:
        print(page)
        url = 'https://www.pulseitmagazine.com.au/search?q={}&w1=before&w2=before&start={}'
        r = session.get(url.format(keyword, page))
        soup1 = BeautifulSoup(r.text, features="html.parser")
        newslist = soup1.findAll('article', class_='uk-article')
        for news in newslist:
            url = news.find('h1', class_='uk-article-title').find('a').attrs['href']
            classifier = url.split('/')[1]
            title = news.find('h1', class_='uk-article-title').find('a').text
            summary = news.find('div').text
            r = session.get('https://www.pulseitmagazine.com.au' + url)
            soup = BeautifulSoup(r.text, features="html.parser")
            date = soup.find('p', class_='uk-article-meta').find('time').text
            date = datetime.datetime.strptime(date, '%d %B %Y')
            year = date.year
            month = date.month
            day = date.day
            print(year, month, day)
            data.append((title, url, summary, (year, month, day), classifier, 'pulseitmagazine'))
            print(title, url, summary, (year, month, day), classifier, 'pulseitmagazine')
        if soup1.find('a', class_='tm-pagination-next'):
            page = page + 20
        else:
            break
extractNewspulseitmagazine('Posture 360')