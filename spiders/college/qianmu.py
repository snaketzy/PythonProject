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
import urllib
from urllib import request
from urllib.parse import quote
import string
from bs4 import BeautifulSoup
import pymysql
import traceback

# 2025排名
url = "http://www.qianmu.org/2025QS世界大学排名"

# http://www.qianmu.org/QS2024工程与技术专业排名
# http://www.qianmu.org/2024QS商科与管理专业排名
# http://www.qianmu.org/2024QS自然科学专业排名
# http://www.qianmu.org/2024QS生命科学与医学专业排名
# http://www.qianmu.org/2024QS艺术与人文科学排名
# http://www.qianmu.org/2024QS电气工程专业排名
# http://www.qianmu.org/2024QS会计与金融专业排名
# http://www.qianmu.org/2024QS数学专业排名
# http://www.qianmu.org/2024QS生物科学专业排名
# http://www.qianmu.org/2024QS传媒专业排名
# http://www.qianmu.org/2024QS建筑学排名
# http://www.qianmu.org/2024QS计算机科学专业排名
# http://www.qianmu.org/2024QS物理专业排名
# http://www.qianmu.org/2024QS医学专业排名
# http://www.qianmu.org/2024QS教育学专业排名
# http://www.qianmu.org/2024QS艺术与设计排名
# http://www.qianmu.org/2024QS机械工程专业排名
# http://www.qianmu.org/2024QS统计学与运筹学排名
# http://www.qianmu.org/2024QS化学专业排名
# http://www.qianmu.org/2024QS心理学专业排名
# http://www.qianmu.org/2024QS政治专业排名
# http://www.qianmu.org/2024QS表演艺术排名
# http://www.qianmu.org/2024QS土木工程专业排名
# http://www.qianmu.org/2024QS经济学与计量经济学排名
# http://www.qianmu.org/2024QS材料科学专业排名
# http://www.qianmu.org/2024QS药剂学与药理学专业排名
# http://www.qianmu.org/2024QS社会学专业排名
# http://www.qianmu.org/2024QS英语语言与文学排名
# http://www.qianmu.org/2024QS化学工程专业排名
# http://www.qianmu.org/2024QS酒店与旅游管理排名
# http://www.qianmu.org/2024QS地球与海洋科学专业排名
# http://www.qianmu.org/2024QS农林科学专业排名
# http://www.qianmu.org/2024QS法学专业排名
# http://www.qianmu.org/2024QS古典文学排名
# http://www.qianmu.org/2024QS采矿工程专业排名
# http://www.qianmu.org/2024QS体育管理排名
# http://www.qianmu.org/2024QS环境科学专业排名
# http://www.qianmu.org/2024QS兽医科学专业排名
# http://www.qianmu.org/2024QS发展研究专业排名
# http://www.qianmu.org/2024QS考古学排名
# http://www.qianmu.org/2024QS石油工程专业排名
# http://www.qianmu.org/2024QS市场营销排名
# http://www.qianmu.org/2024QS地理专业排名
# http://www.qianmu.org/2024QS牙医专业排名
# http://www.qianmu.org/2024QS社会政策与管理排名
# http://www.qianmu.org/2024QS语言学排名
# http://www.qianmu.org/2024QS数据科学专业排名
# http://www.qianmu.org/2024QS地质排名
# http://www.qianmu.org/2024QS护理专业排名
# http://www.qianmu.org/2024QS人类学专业排名
# http://www.qianmu.org/2024QS哲学排名
# http://www.qianmu.org/2024QS地球物理专业排名
# http://www.qianmu.org/2024QS解剖学与生理学专业排名
# http://www.qianmu.org/2024QS图书馆与信息管理排名
# http://www.qianmu.org/2024QS历史排名
# http://www.qianmu.org/2024QS现代语言排名
# http://www.qianmu.org/2024QS艺术史排名
# http://www.qianmu.org/2024QS音乐排名
# http://www.qianmu.org/2024QS神学与宗教排名


specificUrl = 'http://www.qianmu.org/2024QS音乐排名'

# specificUrl = 'http://www.qianmu.org/2018QS%E5%8F%A4%E5%85%B8%E6%96%87%E5%AD%A6%E4%B8%8E%E5%8F%A4%E4%BB%A3%E5%8F%B2%E6%8E%92%E5%90%8D'
# specificUrl = 'http://www.qianmu.org/2019QS世界大学排名'
# specificUrl = urllib.parse.unquote(specificUrl, encoding='utf-8', errors='replace')

'''
获取排名链接
'''
def fetchUrls(url):
    data = request.urlopen(url).read()
    htmlData = BeautifulSoup(data.decode('utf-8'),'html.parser')
    links = htmlData.find_all(href=re.compile("http://www.qianmu.org"),target="_blank")
    # links.append(htmlData.find(href=re.compile("2018QS图书馆信息管理"),target="_blank"))
    # links.append(htmlData.find(href=re.compile("903.htm"),target="_blank"))
    # print(links)
    for index,link in enumerate(links):
        if link.get("href").find("http")!=0:
            link["href"] = "http://www.qianmu.org"+link.get("href")
        print(link.get("href"))
        # getRankDetail(link.get("href"))

'''
获取排名详情
'''
def getRankDetail(url1):
    url1 = urllib.parse.unquote(url1, encoding='utf-8', errors='replace')
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
                print(collegeName)
            else:
                for obj in item.find_all("td")[1]:
                    #url
                    url = ''
                    print(url)
                    #collegeName
                    if str(type(obj)).find("Tag") != -1:
                        collegeName = obj.string
                        print(collegeName)
                    elif obj.__len__() != 0:
                        collegeName = obj.string
                        print(collegeName)
            #englishName
            englishName = item.find_all("td")[2].getText()
            print(englishName)
            #country
            country = item.find_all("td")[3].getText()
            print(country + "\n")

            # database connection test
            db = pymysql.connect("localhost", "root", "snaketzy123$", "qianmu", charset='utf8')
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
            sql = "insert into QS2024(collegeName,collegeEnglishName,collegeCountry,collegeUrl,collegeIntro,collegeRank)\
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

'''
获取年度排名列表
'''
def fetchRankList(url):
    url1 = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
    fp = request.urlopen(quote(url1, safe='/:?=')).read()
    data = BeautifulSoup(fp.decode("utf-8"), "html.parser")
    for index,item in enumerate(data.find_all("tr")):
        if (index != 0):
            # print(item)
            #学校??
            dimension = data.title.getText()[0:data.title.getText().index("-迁木网") - 2]
            print("学校??")
            print(dimension)
            #学校排名
            rank = item.find_all("td")[0].getText()
            print(rank)
            if "2025" in url:
                # 学校URL
                if str(item.find_all("td")[2]).find('href') != -1:
                    # 学校URL
                    collegeUrl = item.find_all("td")[2].find('a').get('href')
                else:
                    # 学校URL
                    collegeUrl = ""
                # 学校名
                collegeName = item.find_all("td")[2].string
                print(collegeName)
                # 学校英文名
                englishName = item.find_all("td")[3].getText().replace("'", "''")
                print(englishName)
                # 学校所属国家
                country = item.find_all("td")[4].getText()
                print(country + "\n")
            else:
                if str(item.find_all("td")[1]).find('href') != -1:
                    # 学校URL
                    collegeUrl = item.find_all("td")[1].find('a').get('href')
                    # 学校名
                    collegeName = item.find_all("td")[1].find('a').getText()
                    print(collegeName)
                else:
                    for obj in item.find_all("td")[1]:
                        # 学校URL
                        collegeUrl = ''
                        print(collegeUrl)
                        # 学校名
                        if str(type(obj)).find("Tag") != -1:
                            collegeName = obj.string
                            print(collegeName)
                        elif obj.__len__() != 0:
                            collegeName = obj.string
                            print(collegeName)
                # 学校英文名
                englishName = item.find_all("td")[2].getText().replace("'", "''")
                print(englishName)
                # 学校所属国家
                country = item.find_all("td")[3].getText()
                print(country + "\n")

            # continue
            # 数据库入库测试
            # database connection test
            db = pymysql.connect(host="localhost", user="root", password="snaketzy123$", database="qianmu", charset='utf8')
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
            sql = "insert into QS2025(collegeName,collegeEnglishName,collegeCountry,collegeUrl,collegeRank)\
                              values('%s','%s','%s','%s','%s')" % \
                  (collegeName, englishName, country, collegeUrl, rank)
            try:
                cursor.execute(sql)
                # print("")
                db.commit()
            except:
                traceback.print_exc()
                db.rollback()
            db.close()


'''
获取专业排名列表
'''
def fetchSpecificRankList(specificUrl):
    url1 = urllib.parse.unquote(specificUrl, encoding='utf-8', errors='replace')
    fp = request.urlopen(quote(url1, safe='/:?=')).read()
    data = BeautifulSoup(fp.decode("utf-8"), "html.parser")
    for index,item in enumerate(data.find_all("tr")):
        if (index != 0):
            # print(item)
            #学校??
            dimension = data.title.getText()[0:data.title.getText().index("-迁木网") - 2]
            print("学校??")
            print(dimension)
            #学校排名
            rank = item.find_all("td")[0].getText()
            print(rank)
            if str(item.find_all("td")[2]).find('href')!=-1:

                # 学校URL
                url =item.find_all("td")[2].find('a').get('href')
                # 学校名
                collegeName = item.find_all("td")[2].find('a').getText()
                print(collegeName)
            else:
                if "音乐" in specificUrl:
                    # 学校URL
                    url = ''
                    print(url)
                    # 学校名
                    collegeName = item.find_all("td")[1].string
                    # 学校英文名
                    englishName = item.find_all("td")[2].getText().replace("'", "''").replace("\\", "")
                    print(englishName)
                    # 学校所属国家
                    country = item.find_all("td")[3].getText()
                    print(country + "\n")
                else:
                    for obj in item.find_all("td")[2]:
                        # 学校URL
                        url = ''
                        print(url)
                        # 学校名
                        if str(type(obj)).find("Tag") != -1:
                            collegeName = obj.string
                            print(collegeName)
                        elif obj.__len__() != 0:
                            collegeName = obj.string
                            print(collegeName)

                    # 学校英文名
                    englishName = item.find_all("td")[3].getText().replace("'", "''").replace("\\", "")
                    print(englishName)
                    # 学校所属国家
                    country = item.find_all("td")[4].getText()
                    print(country + "\n")

            # return
            # 数据库入库测试
            # database connection test
            db = pymysql.connect(host="localhost", user="root", password="snaketzy123$", database="qianmu", charset='utf8')
            cursor = db.cursor()

            sql = "insert into QS2024音乐排名(collegeName,collegeEnglishName,collegeCountry,collegeUrl,collegeRank)\
                              values('%s','%s','%s','%s','%s')" % \
                  (collegeName, englishName, country, "", rank)
            try:
                cursor.execute(sql)
                # print("")
                db.commit()
            except:
                print(collegeName + ", " + englishName)
                traceback.print_exc()
                db.rollback()
            db.close()

'''
数据库入库测试
'''
# def fetchDataBase():
#     # database connection test
#     db = pymysql.connect(host="localhost", user="root", password="snaketzy123$", database="qianmu", charset='utf8')
#     cursor = db.cursor()
#     # cursor.execute("select version()")
#     # data = cursor.fetchone()
#     # print(data)
#     # db.close()
#
#     #
#     # collegeId
#     # collegeName
#     # collegeIntro
#     # collegeEnglishName
#     # collegegCountry
#     # collegeUrl
#     #
#     db.close()

fetchRankList(url)

# fetchSpecificRankList(specificUrl)

# fetchDataBase()

# fetchUrls(url)
# getRankDetail(specificUrl)