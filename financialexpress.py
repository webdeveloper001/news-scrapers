# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewsfinancialexpress(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


    url = 'https://www.financialexpress.com/?s=' + keyword

    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    pagecount = 1
    for pagelink in soup.findAll('a', class_='page-numbers'):
        if pagelink.text != 'Next' and pagecount < int(pagelink.text):
            pagecount = int(pagelink.text)
    print(pagecount)
    for page in range(1, pagecount + 1):
        print(page)
        url = 'https://www.financialexpress.com/page/{}/?s={}'
        r = session.get(url.format(page, keyword))
        soup = BeautifulSoup(r.text, features="html.parser")

        news_list = soup.findAll('div', class_='listitembx')
        for news in news_list:
            title = news.find('h3').find('a').text
            url = news.find('h3').find('a').attrs['href']   
            classifier = url.split('/')[3]
            summary = news.find('h4').text
            print(url)
            r = session.get(url)
            soup = BeautifulSoup(r.text, features="html.parser")
            if soup.find('div', class_='place-line'):
                place_line = soup.find('div', class_='place-line').findAll('span')
                date = place_line[len(place_line) - 1].attrs['content'].split('T')[0]
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            elif soup.find('div', class_='editor'):
                editors = soup.find('div', class_='editor').findAll('span')
                date = editors[len(editors) - 1].attrs['content'].split('T')[0]
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            else:
                date = news.find('span', class_='minsago').text
                date = datetime.datetime.strptime(date, '%b %d, %Y')
            y = date.year
            m = date.month
            d = date.day
            data.append((title, url, summary, (y, m, d), classifier, 'financialexpress'))
            print(title, url, summary, (y, m, d), classifier, 'financialexpress')
    return data
extractNewsfinancialexpress('indo')