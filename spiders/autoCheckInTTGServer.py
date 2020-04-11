from splinter import Browser
import time
from urllib import request
from urllib import parse
import string
import json
from bs4 import BeautifulSoup
import re
import requests


url = 'https://totheglory.im/my.php'
urlCheckIn = 'https://totheglory.im/signed.php'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
    "cookie": "__cfduid=d77857ec53426aa240a9b7aed32a817e91517328913; UM_distinctid=16147daa5ec769-02df05eb2674dc-32657403-fa000-16147daa5ed8cc; __utmz=230798618.1517328968.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1323712766.1517328968; user_info_hash=ace13157de9ebf2051af1eaf585b3d8f; __utma=230798618.1323712766.1517328968.1529110825.1529136981.14; CNZZDATA4085974=cnzz_eid%3D1748487976-1517328159-https%253A%252F%252Ftotheglory.im%252F%26ntime%3D1529133542; uid=31712; pass=d457ebb6ddf19ed25c74a234fa58d76d; laccess=1529598068"
}

urlRequest = request.Request(url=url,headers=headers)
time.sleep(1)
responseData = request.urlopen(urlRequest).read()
time.sleep(1)
responseHTML = BeautifulSoup(responseData.decode("utf-8"),"html.parser")

responseText = str(responseHTML.find_all('script')[6])
timestamp = str(time.time())[0:10]
signed_token = re.search("(signed_token:) (\".*\")",responseText,flags=0).group(2)[1:33]
time.sleep(1)
response = requests.post(urlCheckIn,data={"signed_timestamp": timestamp, "signed_token": signed_token},headers=headers)
time.sleep(1)
print(responseText)
print(signed_token)
print(str(response._content,'utf-8'))
