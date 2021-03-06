# import requests
# import xml.etree.ElementTree as ET
# from xml.parsers.expat import ParserCreate
#
#
# class DefaultSaxHandler(object):
#     def __init__(self,provinces):
#         self.provinces = provinces
#     def  start_element(self,name,attrs):
#         if name == "a":
#             name = attrs['href']
#             #number = attrs['href']
#             self.provinces.append((name))
#     def end_element(self,name):
#         pass
#     def char_data(self,text):
#         pass
#
# def get_provinces_entry(url):
#     #todo
#
#     content = requests.get(url).content.decode("UTF-8")
#
#     start = content.find('<table style=\"width: 954px;\"><tbody>')
#     end = content.find('</tbody></table>')
#     content = content[start:end+len('</tbody></table>')].strip()
#     #print(content)
#
#     provinces = []
#     handler = DefaultSaxHandler(provinces)
#     parser = ParserCreate()
#     parser.StartElementHandler = handler.start_element
#     parser.EndElementHandler = handler.end_element
#     parser.CharacterDataHandler = handler.char_data
#     parser.Parse(content)
#     return provinces
#
# provinces = get_provinces_entry("http://www.qianmu.org/ranking/1528.htm")
# #provinces = get_provinces_entry("http://www.ip138.com/post")
# print(provinces)

import re
import urllib3
from urllib import request
from urllib.parse import quote
import string
from bs4 import BeautifulSoup
import pymysql
import traceback




url = "http://www.qianmu.org/ranking/1528.htm"

specificUrl = 'http://www.qianmu.org/2015QS世界大学排名'

def fetchUrls(url):
    data = request.urlopen(url).read()
    htmlData = BeautifulSoup(data.decode('utf-8'),'html.parser')
    links = htmlData.find_all(href=re.compile("20"),target="_blank")
    for index,link in enumerate(links):
        # print(link.get("href"))
        getRankDetail(link.get("href"))


def getRankDetail(url1):
    fp = request.urlopen(quote(url1,safe='/:?=')).read()
    data = BeautifulSoup(fp.decode("utf-8"),"html.parser")
    # for link in data.find_all(href=re.compile("2018"),target="_blank"):
    #     print([quote(link.get("href"), safe='/:?='),link.get_text()])
    # link = data.find(href=re.compile("20"),target="_blank")
    # print([quote(link.get("href"), safe='/:?='),link.get_text()])

    # fp1 = request.urlopen(quote(link.get("href"), safe='/:?=')).read()
    # data1 = BeautifulSoup(fp1.decode("utf-8"), "html.parser")
    # print(data1.title.getText()[0:data1.title.getText().index("-迁木网")-2])
    for index,item in enumerate(data.find_all("tr")):
        if (index != 0):
            # print(item)
            #dimension
            dimension = data.title.getText()[0:data.title.getText().index("-迁木网") - 2]
            print(dimension)
            #rank
            rank = item.find_all("td")[0].getText()
            print(rank)
            if str(item.find_all("td")[1]).find('href')!=-1:

                # url
                url =item.find_all("td")[1].find('a').get('href')
                # collegeName
                collegeName = item.find_all("td")[1].find('a').getText()
            else:
                for obj in item.find_all("td")[1]:
                    #url
                    url = ''
                    print(url)
                    #collegeName
                    collegeName = obj
                    print(collegeName)

            #englishName
            englishName = item.find_all("td")[2].getText()
            print(englishName)
            #country
            country = item.find_all("td")[3].getText()
            print(country + "\n")

            # database connection test
            db = pymysql.connect("localhost", "root", "snaketzy123$", "Spider", charset='utf8')
            cursor = db.cursor()
            # cursor.execute("select version()")
            # data = cursor.fetchone()
            # print(data)
            # db.close()

            #
            # collegeId
            # collegeName
            # collegeIntro
            # collegeEnglishName
            # collegegCountry
            # collegeUrl
            #
            sql = "insert into qianmu(collegeName,collegeEnglishName,collegeCountry,collegeUrl,collegeDimension,collegeDimensionRank)\
                  values('%s','%s','%s','%s','%s','%s')" % \
                  (collegeName,englishName,country,url,dimension,rank)
            try:
                cursor.execute(sql)
                # print("")
                db.commit()
            except:
                traceback.print_exc()
                db.rollback()
            db.close()

# fetchUrls(url)
getRankDetail(specificUrl)