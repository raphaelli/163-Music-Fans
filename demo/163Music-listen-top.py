#!/usr/bin/env python
# coding: utf-8


import os
import requests
from bs4 import BeautifulSoup


headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
url = "https://music.163.com/#/user/home?id="
user_id = "51135099"
target_Url = url+user_id
ext_html = requests.get(target_Url,headers=headers) 


# !!解决动态加载知识
soup = BeautifulSoup(ext_html.text,'lxml')
songlist = soup.select('span.txt > a > b')
print(songlist)


for songs in urls:
    print(songs)

