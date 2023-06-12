import urllib.parse
import requests
try:
    from scripts.filters.detect_topic import settings
except:
    import sys
    sys.path.append('..')
    import settings

api_token = settings.web_scraping_api_Apikey['api_key']

def get_With_ScrapingApi(url):
    token = api_token
    targetUrl = urllib.parse.quote(url)
    url = "http://api.scrape.do?token={}&url={}".format(token, targetUrl)
    response = requests.request("GET", url)
    print('With Scraping Api Status Code',response.status_code)
    return response.content


if __name__ == '__main__':
    print(api_token)
    pass