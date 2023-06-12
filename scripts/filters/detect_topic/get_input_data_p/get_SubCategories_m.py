import re
import random
from urllib.parse import urlparse
from urllib.parse import ParseResult

import requests
import httpx
from bs4 import BeautifulSoup

try:
    from .get_with_ScrapingApi_m import get_With_ScrapingApi
    from .PreProcess_text import pre_process_TEXT
except:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    import get_with_ScrapingApi_m.get_With_ScrapingApi
    import PreProcess_text.pre_process_SUBCATEGORIES

def expand_url(url):
    p = urlparse(url, 'https')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc
    p = ParseResult('https', netloc, path, *p[3:])
    return (p.geturl())


def get_html(url_in,client):
    ua = f"user_agent = f'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 1000)}.0.0.0 Safari/537.36'"
    headers = {"User-Agent": ua}
    if client == 1:
        if url_in.startswith('http') == False:
            url_in = 'https://www.'+ url_in
        try:
            r = requests.get(str(url_in),headers=headers,verify=False)
            pass
            if r.status_code != 200:
                print(f'Normal Request Status Code: {r.status_code}')
                return get_With_ScrapingApi(url_in)
            return r.content
        except requests.exceptions.ConnectionError:
            url_in = url_in.replace('www.','')
            r = requests.get(str(url_in),headers=headers,verify=False)
            pass
            if r.status_code != 200:
                print(f'Normal Request Status Code: {r.status_code}')
                return get_With_ScrapingApi(url_in)
            return r.content

    if client == 2:
        if url_in.startswith('http') == False:
            url_in = 'https://www.'+ url_in
        try:
            r = httpx.get(url_in)
            if r.status_code == 301:
                r = httpx.get(url_in,follow_redirects=True,verify=False)
            return r.content
        except:
            return

def get_text_in_link(url,links):
    cats = []
    for el in links:
        if url.replace('https://www.','') in el:
            cats.append(str(el).replace(url,'').replace('/',' '))
    return pre_process_TEXT(list(set(cats)))
    # return str(list(set(cats)))

def get_subcategories(url):
    links = []
    html_content = get_html(url,1)
    #HERE I CHECK IF HTML CONTENT IS NONE IF IT IS THEN I ONLY APPEND A RANDOM NR TO LIST IN ORDER FOR PROGRAM TO PROCESS REQUEST WITH HTTPX
    if html_content == None:
        links.append('null')
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            links.append(link['href'])
    if len(links) < 2:
        html_content = get_html(url, 2)
        if html_content != None:
            soup = BeautifulSoup(html_content, 'html.parser')
            for link in soup.find_all('a'):
                if link.has_attr('href'):
                    links.append(link['href'])
        else:
            return 'URL is invalid.'
    if links:
        return get_text_in_link(url,links)
        # return categorize_c(links,url)
    else:
        return 'URL is invalid.'


def type_2(links):
    categories = []
    includes_category = re.compile(r'\/category\/(\w+)([-]\w+)?([-]\w+)?([-]\w+)?[\/]',re.MULTILINE)
    for el in links:
        match = includes_category.search(el)
        if match:
            categories.append(match.group())
    categories = sorted(list(set(categories)))
    if categories:
        return list(el[10:-1] for el in categories)
    else:
        return ["Couldn't Exctract Categories1"]

def type_3(links):
    categories = []
    without_full_link = re.compile(r'^\/\w+([-])?\w+\w+([-])?\w+$', re.MULTILINE)
    for el in links:
        if without_full_link.search(el) != None:
            match = without_full_link.search(el).group()
            categories.append(match[1:len(match)])
    categories = sorted(list(set(categories)))
    if categories:
        return categories
    else:
        return ["Couldn't Exctract Categories2"]

def type_1(links,url):
    categories = []
    link_without_category = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}(\/\w+([-]\w+)?([-]\w+)?([-]\w+)?)([\/])?$', re.MULTILINE)
    for el in links:
        if not url in el:
            continue
        if link_without_category.search(el) != None:
            match = link_without_category.search(el).group()
            match = match[match.find('/',10)+1:len(match)]
            if match[-1] == '/':
                match = match[0:-1]
            categories.append(match)
    categories = sorted(list(set(categories)))
    if categories:
        return categories
    else:
        return ["Couldn't Exctract Categories2"]

def categorize_c(links,url):
    categories = type_1(links,url)
    categories2 = type_2(links)
    if len(categories) >= 3  and len(categories2) >= 3:
        if len(categories) + len(categories2) <= 10:
            return sorted(categories + categories2)
        if len(categories) == len(categories2):
            return categories2
        if len(categories) > len(categories2):
            return categories
        else:
            return categories2
    if len(categories) > 3:
        return categories
    if len(categories2) > 3:
        return categories2
    categories = type_3(links)
    if len(categories) > 3:
        return categories
    return ["Couldn't Exctract Categories"]

if __name__ == '__main__':
    #inputing  the output of this function as a list as raw string  outputs more  accurate results
    print(get_subcategories('https://www.groupenroll.ca'))
    # a = get_subcategories('https://searchtides.com/')
    # print(len(str(set(a))))
    # print(list(set(a)))