# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewsanalyticsindiamag(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


    url = 'https://www.analyticsindiamag.com/?s=' + keyword

    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    
    pagelinkcount = len(soup.findAll('a', class_='page-numbers'))
    if pagelinkcount < 2:
        pagecount = 1
    else:
        pagecount = int(soup.findAll('a', class_='page-numbers')[pagelinkcount - 2].text)
    print(pagecount) 
    for page in range(1, pagecount + 1):
        print(page)
        url = 'https://www.analyticsindiamag.com/page/{}/?s={}'
        r = session.get(url.format(page, keyword))
        soup = BeautifulSoup(r.text, features="html.parser")
        news_list = soup.findAll('div', class_='post')
        for news in news_list:
            classifier = news.find('div', class_='post-category').text
            title = news.find('h5', class_='entry-title').text
            url = news.find('h5', class_='entry-title').find('a').attrs['href']
            # print(classifier, title, url)
            r = session.get(url)
            soup = BeautifulSoup(r.text, features="html.parser")
            date = soup.find('div', class_='time').text
            year = 0
            month = 0
            day = 0
            hour = 0
            minute = 0
            second = 0
            week = 0
            flag = False
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
            else:
                flag =  True
            
            if flag == True:
                day = date.split(' ')[1].replace(',', '')
                if int(day) < 10:
                    day = '0' + day
                date = datetime.datetime.strptime(date.split(' ')[0] + ' ' + day + ', ' + date.split(' ')[2] , '%b %d, %Y')
            else:
                date = datetime.datetime.now()
                date = date + datetime.timedelta(days = -(day + int(week*7) + int(month * 365 / 12) + int(year * 365)) , hours = -hour, minutes = -minute, seconds = -second)
            y = date.year
            m = date.month
            d = date.day
            summary = soup.find('div', class_='post-content').findAll('p')[1].text
            data.append((title, url, summary, (y, m, d), classifier, 'analyticsindiamag'))
            print(title, url, summary, (y, m, d), classifier, 'analyticsindiamag')
    return data
extractNewsanalyticsindiamag('Posture 360')