# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewschannelnewsasia(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })

    url = 'https://www.channelnewsasia.com/blueprint/servlet/action/news/8396414/search?query=' + keyword

    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    if soup.find('p', class_='result-section__index'):
        total = int(soup.find('p', class_='result-section__index').findAll('strong')[1].text)
    else:
        total = 1
    print(total)
    pagecount = int(total / 10) + 1
    for page in range(0, pagecount):
        url = 'https://www.channelnewsasia.com/blueprint/servlet/action/news/8396414/search?query={}&pageNum={}'
        r = session.get(url.format(keyword, page))
        soup = BeautifulSoup(r.text, features="html.parser")
        news_list = soup.findAll('div', class_='c-teaser--result')
        for news in news_list:
            classifier = news.find('a', class_='teaser__category').text
            title = news.find('a', class_='teaser__title').text
            url = 'https://www.channelnewsasia.com' + news.find('a', class_='teaser__title').attrs['href']
            print(url)
            r = session.get(url.format(keyword, page))
            soup = BeautifulSoup(r.text, features="html.parser")
            if len(soup.findAll('div', class_='c-rte--article')) >= 1:
                summary = soup.findAll('div', class_='c-rte--article')[0].findAll('p')[0].text
            elif len(soup.findAll('div', class_='c-rte--light')) >= 1:
                summary = soup.findAll('div', class_='c-rte--light')[0].findAll('p')[0].text
            elif soup.find('div', class_='teaser-text'):
                summary = soup.find('div', class_='teaser-text').text
            else:
                summary = ''
            if soup.find('time', class_='article__details-item'):
                date = soup.find('time', class_='article__details-item').text
                date = datetime.datetime.strptime(date.replace(date.split(' ')[3], '').strip(), '%d %b %Y')
            elif soup.find('time', class_='video-stage__details-item'):
                date = soup.find('time', class_='video-stage__details-item').text
                date = datetime.datetime.strptime(date.replace(date.split(' ')[3], '').strip(), '%d %b %Y')
            else:
                date = datetime.datetime.now()
            year = date.year
            month = date.month
            day = date.day
            data.append((title, url, summary, (year, month, day), classifier, 'channelnewsasia'))
            print(title, url, summary, (year, month, day), classifier, 'channelnewsasia')
    
    return data
extractNewschannelnewsasia('Dr Kitchen')