import re
import urllib3
import os
from urllib import request
from urllib.parse import quote
import string
import json
from bs4 import BeautifulSoup

url1 = "https://xinya.me/experience_albums/17"

fp = request.urlopen(url1).read()
data = BeautifulSoup(fp.decode("utf-8"),"html.parser")
dataContent = data.find("div",attrs={"data-react-class":"experience_albums/ExperienceAlbumSections"}).get("data-react-props")

jsonData = json.loads(dataContent)

def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print(per)

print(dataContent)
print(os.getcwd())
#os.makedirs(os.getcwd()+"/"+data.title.get_text())
print("\n")

print(data.title.get_text())

for items in jsonData["sections"]:
    #os.makedirs(os.getcwd() + "/" + data.title.get_text()+"/"+items["name"])
    print("\n"+items["name"])
    for item in items["audios"]:
        #localUrl = os.getcwd() + "/" + data.title.get_text()+"/"+items["name"]+"/"+item["user_name"] + "-" + item["name"]+".mp3"
        #request.urlretrieve(item["src"], localUrl,Schedule)
        #print(localUrl)
        print([item["user_name"] + "-" + item["name"], item["src"]])