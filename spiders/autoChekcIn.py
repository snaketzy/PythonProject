from splinter import Browser
import time
from urllib import request
from urllib import parse
import string
import json
from bs4 import BeautifulSoup
import re


url = 'http://hdhome.org/'
urlCheckIn = 'https://hdhome.org/attendance.php'
dicts = {
    "__cfduid":"d62c67249fcaed37080ede9d7a933c5cf1529470692",
    "c_secure_login":"bm9wZQ%3D%3D",
    "c_secure_pass":"de169a78693d815b7fc014a2ef23130c",
    "c_secure_ssl":"bm9wZQ%3D%3D",
    "c_secure_tracker_ssl":"bm9wZQ%3D%3D",
    "c_secure_uid":"MTAxMzAy"
}
browser = Browser('chrome')
browser.visit(url)
browser.cookies.add(dicts)
browser.visit(urlCheckIn)
print(browser.cookies.all())
time.sleep(5)
# while(1):
#     browser.find_by_name('username').fill('snaketzy')
#     browser.find_by_name('password').fill('snaketzy123$')
#     time.sleep(10)
#     browser.find_by_value('登录').click()
#     time.sleep(10)
#     browser.visit(urlCheckIn)
browser.quit()



#
# headers = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "cache-control": "max-age=0",
#     "cookie": "__cfduid=d920b0941d5bceb5c2ae96cf8f09bf9661529474621; __cfduid=d62c67249fcaed37080ede9d7a933c5cf1529470692; c_secure_login=bm9wZQ%3D%3D; c_secure_pass=de169a78693d815b7fc014a2ef23130c; c_secure_ssl=bm9wZQ%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_uid=MTAxMzAy",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
# }
#
# urlRequest = request.Request(url=url)
# response = request.urlopen(url).read()
# data = BeautifulSoup(response.decode("utf-8"),"html.parser")
# print(data)