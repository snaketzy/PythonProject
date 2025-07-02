# import requests
# import xml.etree.ElementTree as ET
# from xml.parsers.expat import ParserCreate
import random

print("年会抽奖开始")
stuff0=list(range(1,11))  #职工300人
print(stuff0)

third=random.sample(stuff0,2)     #抽出三等奖30人
print("恭喜三等奖获得者")
print(third)

for stuff in third:
    stuff0.remove(stuff)
print(stuff0)