# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewszdnet(keyword):
    print(keyword)
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


    url = 'https://www.zdnet.com/search/?o=0&q=' + keyword

    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    pagecount = 1
    if soup.find('nav', class_='pagination'):
        for pagelink in soup.find('nav', class_='pagination').findAll('a'):
            if pagelink.text != 'Next' and pagecount < int(pagelink.text):
                pagecount = int(pagelink.text)
    newslist = soup.findAll('article', class_='item')
    for news in newslist:
        title = news.find('h3').find('a').text
        url = news.find('h3').find('a').attrs['href']
        classifier = url.split('/')[1]
        url = 'https://www.zdnet.com' + url
        summary = news.find('div', class_='content').find('p').text

        r = session.get(url)
        soup = BeautifulSoup(r.text, features="html.parser")
        year = ''
        date = ''
        day = ''
        date = datetime.datetime.now()            
        if soup.find('p', class_='meta'):
            if soup.find('p', class_='meta').find('time'):
                date = datetime.datetime.strptime(soup.find('p', class_='meta').find('time').attrs['datetime'].split(' ')[0], '%Y-%m-%d')
        year = date.year
        month = date.month
        day = date.day
        data.append((title, url, summary, (year, month, day), classifier, 'zdnet'))
        print(title, url, summary, (year, month, day), classifier, 'zdnet')
    for page in range(2, pagecount + 1):
        print(page)
        url = 'https://www.zdnet.com/search/{}/?o=0&q={}'
        r = session.get(url.format(page, keyword))
        soup = BeautifulSoup(r.text, features="html.parser")
        newslist = soup.findAll('article', class_='item')
        for news in newslist:
            title = news.find('h3').find('a').text
            url = news.find('h3').find('a').attrs['href']
            classifier = url.split('/')[1]
            print(url)
            url = 'https://www.zdnet.com' + url
            summary = news.find('div', class_='content').find('p').text


            r = session.get(url)
            soup = BeautifulSoup(r.text, features="html.parser")
            year = ''
            date = ''
            day = ''
            date = datetime.datetime.now()            

            if soup.find('p', class_='meta'):
                if soup.find('p', class_='meta').find('time'):
                    date = datetime.datetime.strptime(soup.find('p', class_='meta').find('time').attrs['datetime'].split(' ')[0], '%Y-%m-%d')
       
            year = date.year
            month = date.month
            day = date.day
            data.append((title, url, summary, (year, month, day), classifier, 'zdnet'))
            print(title, url, summary, (year, month, day), classifier, 'zdnet')
    print(pagecount)
    return data

print(extractNewszdnet('Posture 360'))
print(extractNewszdnet('Medipass'))
print(extractNewszdnet('Well Being Digital'))
print(extractNewszdnet('Awair'))
print(extractNewszdnet('Cottonsoil'))
print(extractNewszdnet('GymT'))
print(extractNewszdnet('Smartmissimo'))
print(extractNewszdnet('PregBuddy'))
print(extractNewszdnet('Iridium Medical Technology'))
print(extractNewszdnet('hayylo'))
print(extractNewszdnet('Magqu'))
print(extractNewszdnet('HealthKit'))
print(extractNewszdnet('DentalTap'))
print(extractNewszdnet('MediPixel'))
print(extractNewszdnet('Diagme'))
print(extractNewszdnet('VieVie'))
print(extractNewszdnet('PROVIGATE'))
print(extractNewszdnet('Ybrain'))
print(extractNewszdnet('Pharmarack'))
print(extractNewszdnet('qoctor'))
print(extractNewszdnet('GP2U Telehealth'))
print(extractNewszdnet('Global Health and Travel'))
print(extractNewszdnet('Misfit Wearables'))
print(extractNewszdnet('Medifi'))
print(extractNewszdnet('OneBreath'))
print(extractNewszdnet('Hello Bacsi'))
print(extractNewszdnet('ClinMD'))
print(extractNewszdnet('PesanLab'))
print(extractNewszdnet('Tweet2Health'))
print(extractNewszdnet('365Doctor'))
print(extractNewszdnet('Allis Technology'))
print(extractNewszdnet('SmartHealthCare'))
print(extractNewszdnet('CohereMed'))
print(extractNewszdnet('MetaOptima'))
print(extractNewszdnet('Lucence Diagnostics'))
print(extractNewszdnet('iXensor'))
print(extractNewszdnet('Brainpan'))


