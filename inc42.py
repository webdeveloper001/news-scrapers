# -*- coding: utf-8 -*-
import csv     
import requests
import json
import datetime
from bs4 import BeautifulSoup 
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def extractNewsinc42(keyword):
    data = []

    session = requests.Session()
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })


    url = 'https://vzw3knfv02-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.21.1%3Binstantsearch.js%201.11.15%3BJS%20Helper%202.19.0&x-algolia-application-id=VZW3KNFV02&x-algolia-api-key=0d26d2598038e74fbaa0325128dad9f2'
    r = session.post(url, data = json.dumps({"requests":[{"indexName":"wp_searchable_posts","params":"query={}&hitsPerPage=10&page={}&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&facetingAfterDistinct=true&facets=%5B%5D&tagFilters=".format(keyword, 0)}]}))
    resp = json.loads(r.text)
    pagecount = resp['results'][0]['nbPages']
    for page in range(0, pagecount):
        print(page)
        url = 'https://vzw3knfv02-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.21.1%3Binstantsearch.js%201.11.15%3BJS%20Helper%202.19.0&x-algolia-application-id=VZW3KNFV02&x-algolia-api-key=0d26d2598038e74fbaa0325128dad9f2'
        r = session.post(url, data = json.dumps({"requests":[{"indexName":"wp_searchable_posts","params":"query={}&hitsPerPage=10&page={}&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&facetingAfterDistinct=true&facets=%5B%5D&tagFilters=".format(keyword, page)}]}))
        resp = json.loads(r.text)
        for news in resp['results'][0]['hits']:
            summary = news['content']
            classifier = news['post_type_label']
            title = news['post_title']
            url = news['permalink']
            date = datetime.datetime.strptime(news['post_date_formatted'], '%B %d, %Y')
            year = date.year
            month = date.month
            day = date.day
            data.append((title, url, summary, (year, month, day), classifier, 'inc42'))
            print(title, url, summary, (year, month, day), classifier, 'inc42')
    return data
extractNewsinc42('indo')