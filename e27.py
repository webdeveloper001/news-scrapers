# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewse27(keyword):

    data = []
    session = requests.Session()
    
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Cookie': '__cfduid=dfc8174aa939247f28b8e57225762cf761567761638; PHPSESSID=uscg5f8hvujvglvb9bmpfj0m41; reset_cookie=1; _ga=GA1.2.519143530.1567761640; _gid=GA1.2.76823614.1567761640; signUpModalShown=1567761641; _fbp=fb.1.1567761643684.1365921979; _yeti_currency_2={"dataAsOf":"2019-09-05T10:00:54.097Z","conversions":{"USD":{"CAD":1.33227446,"HKD":7.8407151933,"ISK":126.4294790343,"PHP":51.9195861318,"DKK":6.7692866219,"HUF":298.5478308223,"CZK":23.4470865856,"GBP":0.8191595571,"RON":4.2920675259,"SEK":9.7594844799,"IDR":14152.4959157742,"INR":72.0539117807,"BRL":4.1389544382,"RUB":66.3941731712,"HRK":6.7203666727,"JPY":106.2170992921,"THB":30.6153566891,"CHF":0.9845707025,"EUR":0.9076057361,"MYR":4.1997640225,"BGN":1.7750952986,"TRY":5.6709021601,"CNY":7.1526592848,"NOK":9.0613541478,"NZD":1.5740606281,"ZAR":14.8601379561,"USD":1,"MXN":19.8248320929,"SGD":1.385913959,"AUD":1.4725903068,"ILS":3.5249591577,"KRW":1205.2641132692,"PLN":3.9385550917},"GBP":{"CAD":1.6263918896,"HKD":9.5716580799,"ISK":154.3404797518,"PHP":63.3815301091,"DKK":8.2636973021,"HUF":364.4562628109,"CZK":28.623344967,"GBP":1,"RON":5.2395989142,"SEK":11.9140213839,"IDR":17276.8489280372,"INR":87.9607777962,"BRL":5.0526840618,"RUB":81.05157609,"HRK":8.203977619,"JPY":129.665946485,"THB":37.3741066977,"CHF":1.201927871,"EUR":1.1079718575,"MYR":5.1269181763,"BGN":2.1669713589,"TRY":6.9228297601,"CNY":8.7317046147,"NOK":11.0617694311,"NZD":1.9215555925,"ZAR":18.1407124259,"USD":1.2207633926,"MXN":24.2014292837,"SGD":1.6918730264,"AUD":1.7976843388,"ILS":4.3031411002,"KRW":1471.3423079054,"PLN":4.8080438757}}}; __gads=ID=c84b1d8fe6aef86a:T=1567761651:S=ALNI_MYn3DGbC_gFQhoepAeSoRVU-D6Yeg; ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22dae027a42a83e128cdb1b59afe6b1462%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A7%3A%220.0.0.0%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A115%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F76.0.3809.132+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1567763082%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D3e56e2c946400ce18041eb2f2ef90647'
    })

    url = 'https://e27.co/search/articles/?s=' + keyword
    r = session.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    total = soup.findAll('a', class_='latest-title-list')[0].text.replace('ARTICLES (', '').replace(' results) ', '').replace(' result) ', '')
    pagecount = int(int(total) / 10) + 1
    print(pagecount)
    for page in range(1, pagecount + 1):
        url = 'https://e27.co/search/ajax_search_articles/?all&s={}&per_page={}'
        r = session.get(url.format(keyword, page))
        # print(r.text)
        content = r.text
        if len(r.text.split('}<div')) == 2:
            content = r.text.split('}<div')[0] + '}'
        print(content)
        soup = BeautifulSoup(json.loads(content)['content'], features="html.parser")
        news_list = soup.findAll('div', class_='mbt-m')
        for news in news_list:
            classifier = news.find('a', class_='cat-img-overlay').text
            title = news.find('h2', class_='list-article-title').text
            url = news.findAll('a')[0].attrs['href']
            r = session.get(url + '/?json')
            soup = BeautifulSoup(r.text, features="html.parser")
            summary = soup.find('h2', class_='post-subheading').text.strip()
            date = datetime.datetime.strptime(soup.find('div', class_='post-date').text, ', %d %b, %Y')
            year = date.year
            month = date.month
            day = date.day
            data.append((title, url, summary, (year, month, day), classifier, 'e27'))
            print(title, url, summary, (year, month, day), classifier, 'e27')
    return data
extractNewse27('Dr Kitchen')