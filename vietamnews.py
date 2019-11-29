# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewsvietnamnews(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


    url = 'http://vietnamnews.com/search?search=' + keyword

    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    pagecount = 1
    if soup.find('ul', class_='pagination'):
        for pagelink in soup.find('ul', class_='pagination').findAll('a'):
            if pagelink.text != '»' and pagelink.text != '»' and pagecount < int(pagelink.text):
                pagecount = int(pagelink.text)

    for page in range(1, pagecount + 1):
        print(page)
        url = 'http://vietnamnews.com/search?search={}&page={}'
        r = session.get(url.format(keyword, page))
        soup = BeautifulSoup(r.text, features="html.parser")
        newslist = soup.findAll('article', class_='simple-post')
        print(len(newslist))
        for news in newslist:
            title = news.find('h3').find('a').text.strip()
            url = 'http://vietnamnews.com' + news.find('h3').find('a').attrs['href']
            classifier = news.find('p', class_='simple-share').findAll('a')[0].text
            summary = news.find('p', class_='excerpt').text.strip()
            
            year = 0
            month = 0
            day = 0
            hour = 0
            minute = 0
            second = 0
            week = 0
            date = news.find('p', class_='simple-share').find('span').text.strip()
            print(date)
            if 'year' in date:
                year = int(date.split(' ')[0])
            elif 'month' in date:
                month = int(date.split(' ')[0])
            elif 'day' in date:
                day = int(date.split(' ')[0])
            elif 'hour' in date:
                hour = int(date.split(' ')[0])
            elif 'minute' in date:
                minute = int(date.split(' ')[0])
            elif 'second' in date:
                second = int(date.split(' ')[0])
            elif 'week' in date:
                week = int(date.split(' ')[0])

            date = datetime.datetime.now()
            date = date + datetime.timedelta(days = -(day + int(week*7) + int(month * 365 / 12) + int(year * 365)) , hours = -hour, minutes = -minute, seconds = -second)
            y = date.year
            m = date.month
            d = date.day
            data.append((title, url, summary, (y, m, d), classifier, 'vietamnews'))
            print(title, url, summary, (y, m, d), classifier, 'vietamnews')
extractNewsvietnamnews('VieVie')