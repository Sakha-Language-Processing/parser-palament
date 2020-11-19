import requests
from bs4 import BeautifulSoup

def find_all_urls(url):
    page = requests.get(url) 
    if page.status_code == 200:
        try:
            soup = BeautifulSoup(page.text, "lxml")
            urls_articles = []
            parts = soup.find_all("a", {"itemprop": "url"})
            for part in parts:
                 urls_articles += ['https://www.sakhaparliament.ru' + part['href']]
            return urls_articles
        except Exception as exc:
            return []
    else:
        print('code is not 200')
        return []   

address = 'https://www.sakhaparliament.ru/sa/sonunnar-bary'
list_of_urls = []
for i in range(10000):
    if i==0:
        nextpage = find_all_urls(address)
    else: 
        nextpage = find_all_urls(address + '?start='+str(i*20))
    if nextpage!=[]:
        list_of_urls += nextpage
    else:    
        break          
textfile = "sakha_parlament_urls.txt"
with open(textfile, 'w') as f:
    f.write("\n".join(list_of_urls))      

with open(textfile, 'r') as f:
    mystring = f.read()
list_of_urls2 = mystring.split("\n")   

raw_data_list = []
for url in list_of_urls2:
    cur_article = {}
    page = requests.get(url)
    sp = BeautifulSoup(page.content, 'html.parser')
    cur_article['url'] = url
    cur_article['raw_text'] = [_.get_text().replace("\xa0", " ") for _ in sp.find_all('p')][:-2]
    raw_data_list.append(cur_article)

import json
with open('raw_data_parlamentsakha.json', 'w') as outfile:
    json.dump(raw_data_list, outfile, ensure_ascii=False)