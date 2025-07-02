import re
import urllib3
import urllib
from urllib import request
from urllib.parse import quote
import string
from bs4 import BeautifulSoup
import pymysql
import traceback

# 斯坦福
specificUrl = 'http://www.qianmu.org/%E6%96%AF%E5%9D%A6%E7%A6%8F%E5%A4%A7%E5%AD%A6'

'''
获取学校详情
'''
def getSchoolDetail(url):
    url1 = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
    fp = request.urlopen(quote(url1,safe='/:?=')).read()
    data = BeautifulSoup(fp.decode("utf-8"),"html.parser")

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


getSchoolDetail(specificUrl)