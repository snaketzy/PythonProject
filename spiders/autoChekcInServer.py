from splinter import Browser
import time
from urllib import request
from urllib import parse
import string
import json
from bs4 import BeautifulSoup
import re


url = 'https://hdhome.org'
urlCheckIn = 'https://hdhome.org/attendance.php'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
    "cookie": "__cfduid=d920b0941d5bceb5c2ae96cf8f09bf9661529474621; __cfduid=d62c67249fcaed37080ede9d7a933c5cf1529470692; c_secure_login=bm9wZQ%3D%3D; c_secure_pass=de169a78693d815b7fc014a2ef23130c; c_secure_ssl=bm9wZQ%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_uid=MTAxMzAy"
}

urlRequest = request.Request(url=urlCheckIn,headers=headers)
response = request.urlopen(urlRequest).read()
data = BeautifulSoup(response.decode("utf-8"),"html.parser")
print(data)