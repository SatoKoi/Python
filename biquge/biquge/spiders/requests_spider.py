# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import os
import re
# ret = 2
# if 1 <= ret <= 2:
#     print ret

url = 'http://www.biquge5200.com/14_14615/'
resp = requests.get(url)
resp.encoding = 'gb2312'
# print resp.text.replace("<br>", '').replace("</br>", '')
soup = bs(resp.text, 'html.parser')
# category = soup.find('div', class_='con_top').find_all('a')[2]
# print category.get_text()
# print soup.find('h1')
# dds = soup.find_all('dd')[9:-1]
# url_set = set()
# for dd in dds:
#     chapter_name = dd.find('a').get_text()
#     chapter_id = re.search(r'/(\d+)\.html', str(dd)).group(1)
    # chapter_url = dd.find('a')['href']
    # print chapter_url
    # print chapter_id

# print str(soup)
# with open(os.getcwd() + '/source.txt', 'w+') as f_obj:
#     f_obj.write(str(soup))
novel_lists = soup.find_all('div', class_='novellist')
for novel_list in novel_lists:
    list_name = novel_list.find('h2').get_text()
    list_novels = novel_list.find_all('a')
    print(list_name)
    for list_novel in list_novels:
        print(list_novel['href'])

