import re
import urllib3
import os
from urllib import request
from urllib.parse import quote
import string
import json
from bs4 import BeautifulSoup
import pdfkit

listUrl = "http://chuansong.me/account/FeZaoDuKe"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
    "cookie": "__cfduid=d920b0941d5bceb5c2ae96cf8f09bf9661529474621; __cfduid=d62c67249fcaed37080ede9d7a933c5cf1529470692; c_secure_login=bm9wZQ%3D%3D; c_secure_pass=de169a78693d815b7fc014a2ef23130c; c_secure_ssl=bm9wZQ%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_uid=MTAxMzAy"
}
urlsArray = []

urlsArrayIndex = 0

while urlsArrayIndex < 1645:
    urlsArray.append("http://chuansong.me/account/FeZaoDuKe?start="+str(urlsArrayIndex))
    urlsArrayIndex += 12

def getArticleContent(url):
    urlRequest = request.Request(url=listUrl, headers=headers)
    fp = request.urlopen(urlRequest).read()
    data = BeautifulSoup(fp.decode("utf-8"), "html.parser")
    print(data)

def getArticleUrl(url):
    urlRequest = request.Request(url=listUrl,headers=headers)
    fp = request.urlopen(urlRequest).read()
    data = BeautifulSoup(fp.decode("utf-8"),"html.parser")
    articleUrls = data.find_all(href=re.compile('/n/'))
    for index,item in enumerate(articleUrls):
        getArticleContent("http://chuansong.me"+item.get("href"))

for index, item in enumerate(urlsArray):
    # getArticleUrl(item)
    print("")

getArticleUrl("http://chuansong.me/account/FeZaoDuKe?start=0")