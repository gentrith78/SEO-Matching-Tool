import urllib.parse
import requests

from bs4 import BeautifulSoup
from langdetect import detect

import sys
sys.path.append('..')
import settings

def is_english(url):
    token = settings.web_scraping_api_Apikey['api_key']
    targetUrl = urllib.parse.quote(url)
    url = "http://api.scrape.do?token={}&url={}".format(token, targetUrl)
    response = requests.request("GET", url)
    if response.status_code < 250:
        soup = BeautifulSoup(response.text, features='html.parser')
        p_tags = []
        h_tags = []
        for p in soup.find_all('p'):
            p_tags.append(p.text)
        for h in soup.find_all('h1'):
            h_tags.append(h.text)
        for h in soup.find_all('h2'):
            h_tags.append(h.text)
        for h in soup.find_all('h3'):
            h_tags.append(h.text)
        for h in soup.find_all('h4'):
            h_tags.append(h.text)
        language = ''
        if p_tags or h_tags:
            if len(p_tags) > 3:
                language = detect('. '.join(p_tags))
                return language
            else:
                language = detect('. '.join(p_tags + h_tags))
                return language
        return ''
    return ''
