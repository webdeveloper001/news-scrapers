# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewsmgronline(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


    url = 'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=1&hl=th&source=gcsc&gss=.com&cselibv=c96da2eab22f03d8&cx=partner-pub-8279800357867630:9171142273&q={}&safe=active&cse_tok=AKaTTZip0N7YpVfvUuQ8eDsWMcUj:1568285929175&sort=date&exp=csqr,4229469&callback=google.search.cse.api12564'
    r = session.get(url.format(keyword))
    resp = json.loads(r.text.replace(');', '').replace('google.search.cse.api12564(', '').replace('/*O_o*/', ''))
    totalcount = 0
    if 'cursor' in resp:
        totalcount = int(resp['cursor']['estimatedResultCount'])
    pagecount = int(int(totalcount) / 10) + 1
    for page in range(0, pagecount):
        print(page)
        url = 'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&start={}&hl=th&source=gcsc&gss=.com&cselibv=c96da2eab22f03d8&cx=partner-pub-8279800357867630:9171142273&q={}&safe=active&cse_tok=AKaTTZip0N7YpVfvUuQ8eDsWMcUj:1568285929175&sort=date&exp=csqr,4229469&callback=google.search.cse.api12564'
        r = session.get(url.format(page*10, keyword))
        resp = json.loads(r.text.replace(');', '').replace('google.search.cse.api12564(', '').replace('/*O_o*/', ''))
        if 'results' in resp:
            newslist = resp['results']
            for news in newslist:
                url = news['formattedUrl']
                classifier = news['formattedUrl'].split('/')[3]
                title = news['title']
                summary = news['content'].split('...')[0].strip()
                date = news['richSnippet']['metatags']['articlePublishedTime'].split(' ')[0]
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
                y = date.year
                m = date.month
                d = date.day
                data.append((title, url, summary, (y, m, d), classifier, 'mgronline'))
                print(title, url, summary, (y, m, d), classifier, 'mgronline')

    return data
extractNewsmgronline('Brainpan')