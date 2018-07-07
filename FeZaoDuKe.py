import re
import urllib3
import os
from urllib import request
from urllib.parse import quote
import string
import json
from bs4 import BeautifulSoup

listUrl = "https://mp.weixin.qq.com/profile?src=3&timestamp=1529746670&ver=1&signature=07VDeMiUAG0av39cka13COjcq44y7n*Dm-SQWhg5*7Gb5Fti6yPqZHgtbdE-AqvRX4rnhwXGfYKiYaJpvZKz5A=="

fp = request.urlopen(listUrl).read()
data = BeautifulSoup(fp.decode("utf-8"),"html.parser")
dataContent = data.find("div",attrs={"data-react-class":"experience_albums/ExperienceAlbumSections"}).get("data-react-props")

jsonData = json.loads(dataContent)

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