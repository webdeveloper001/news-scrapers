# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewstechnode(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


    url = 'https://technode.com/?s=' + keyword

    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    pagecount = 1
    for pagelink in soup.findAll('a', class_='page-numbers'):
        if pagecount < int(pagelink.text):
            pagecount = int(pagelink.text)
    print(pagecount)
    # print(pagecount)
    for page in range(1, pagecount + 1):
        print(page)
        url = 'https://technode.com/page/{}/?s={}'
        r = session.get(url.format(page, keyword))
        soup = BeautifulSoup(r.text, features="html.parser")
        news_list = soup.findAll('article')
        for news in news_list:
            title = news.find('h1', class_='entry-title').find('a').text
            url = news.find('h1', class_='entry-title').find('a').attrs['href']
            summary = news.find('div', class_='entry-summary').text
            print(url)
            year = ''
            month = ''
            day = ''
            if len(url.split('/')[3]) == 4:
                year = int(url.split('/')[3])
                month = int(url.split('/')[4])
                day = int(url.split('/')[5])
            r = session.get(url)
            
            soup = BeautifulSoup(r.text, features="html.parser")
            classifier = ''
            if soup.find('div', class_='category-info'):
                classifier = soup.find('div', class_='category-info').find('a').text
            data.append((title, url, summary, (year, month, day), classifier, 'technode'))
            print(title, url, summary, (year, month, day), classifier, 'technode')
    return data
extractNewstechnode('indo')