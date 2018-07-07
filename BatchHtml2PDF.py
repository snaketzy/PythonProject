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