import requests

from bs4 import BeautifulSoup


from .get_with_ScrapingApi_m import get_With_ScrapingApi
from .PreProcess_text import pre_process_TEXT


def get_html_text(html_m):
    final_output = []
    soup = BeautifulSoup(html_m,features='html.parser')
    for h in soup.find_all(['h1', 'h2', 'h3']):
        if not h.text.isspace() or h.text.isdigit():
            final_output.append(h.text.rstrip().rstrip().replace('  ','').replace('\n',""))
    for p in soup.find_all('p'):
        if not p.text.isspace() or p.text.isdigit():
            final_output.append(p.text.rstrip().rstrip().replace('  ','').replace('\n',""))
    for l in soup.find_all('li'):
        if not l.text.isspace() or l.text.isdigit():
            final_output.append(l.text.rstrip().rstrip().replace('  ','').replace('\n',""))
    for td in soup.find_all('td'):
        if not td.text.isspace() or td.text.isdigit():
            final_output.append(td.text.rstrip().rstrip().replace('  ', '').replace('\n',""))
    # return list(set(final_output))
    return pre_process_TEXT(list(set(final_output)))
    # return list(set(final_output))

def get_MainPage_text(url_in):
    if url_in.startswith('http') == False:
        url_in = 'https://www.' + url_in
    #return html content
    r = requests.get(url_in)
    if r.status_code != 200:

        return get_html_text(get_With_ScrapingApi(url_in))
    return get_html_text(r.content)
if __name__ == '__main__':
    print(get_MainPage_text('https://www.horseracingqa.com/'))