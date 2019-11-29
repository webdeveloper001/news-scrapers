# -*- coding: utf-8 -*-
import csv     
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewslivemint(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Cookie': 'ident-stat=location=NA,date=1567671669,accepted=0; _ga=GA1.2.1948912775.1567671668; _gid=GA1.2.763229530.1567671668; _cb_ls=1; new_script=true; _cb=SBzvtBVwIdMS9Ljs; _domain_fp_id=d2cbe875-58bc-4675-875f-630f18e1ee6e; _ht_fp=d2cbe875-58bc-4675-875f-630f18e1ee6e; ht_push_do_not_show_notification_popup=true; _sp_ses.9d0c=*; _cb_svref=null; _ht_notify_firstTime=1567627055; _chartbeat5=; _chartbeat2=.1567671672318.1567681010402.1.B4-BthCYmR5uSE6HV_3LcCDit3nz.20; _sp_id.9d0c=c98a708e-5f9d-427f-908f-331f1861e1c1.1567671673.2.1567681011.1567671712.93f28e23-14f3-4621-ae27-ea3b04df399c'
    })


    url = 'https://www.livemint.com/Search/Link/Keyword/' + keyword

    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    total = int(soup.find('div', class_='listingSearch').find('strong').text.replace(',',''))
    pagecount = int(total / 10) + 1
    for page in range(0, pagecount):
        url = 'https://www.livemint.com/searchlisting/{}/{}'
        r = session.get(url.format(page, keyword))
        soup = BeautifulSoup(r.text, features="html.parser")
        news_list = soup.findAll('div', class_='listing')
        for news in news_list:
            title = news.find('h2', class_='headline').find('a').text
            url = news.find('h2', class_='headline').find('a').attrs['href']
            classifier = url.split('/')[1]
            url = 'https://www.livemint.com' + url
            datecount = len(news.find('span', class_='date').findAll('span'))
            date = news.find('span', class_='date').findAll('span')[datecount - 1].attrs['data-updatedtime'].split('T')[0]
            date = datetime.strptime(date, '%Y-%m-%d')
            year = date.year
            month = date.month
            day = date.day

            r = session.get(url)
            soup = BeautifulSoup(r.text, features="html.parser")
            article = soup.findAll('article')[0]
            if article.find('p', class_='summary'):
                summary = article.find('p', class_='summary').text
            else:
                summary = article.find('ul', class_='highlights').text
            data.append((title, url, summary, (year, month, day), classifier, 'Livemint'))
            print(title, url, summary, (year, month, day), classifier, 'Livemint')
    return data
print(extractNewslivemint('indo'))