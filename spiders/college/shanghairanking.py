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
url = "http://www.shanghairanking.cn/rankings/bcur/2025"

'''
获取年度排名列表
'''
def fetchRankList(url):
    url1 = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
    fp = request.urlopen(quote(url1, safe='/:?=')).read()
    data = BeautifulSoup(fp.decode("utf-8"), "html.parser")
    for index,item in enumerate(data.find_all("tr")):
        if (index != 0):
            print(item)
            #学校排名
            rank = item.find_all("td")[0].getText()
            print(rank)
            if str(item.find_all("td")[1]).find('href')!=-1:

                # 学校URL
                url =item.find_all("td")[1].find('a').get('href')
                # 学校名
                collegeName = item.find_all("td")[1].find('a').getText()
                print(collegeName)
            else:
                for obj in item.find_all("td")[1]:
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


            return
            # 数据库入库测试
            # database connection test
            db = pymysql.connect(host="localhost", user="root", password="snaketzy123$", database="shanghairanking", charset='utf8')
            cursor = db.cursor()

            sql = "insert into QS2025(collegeName,collegeEnglishName,collegeCountry,collegeUrl,collegeRank)\
                              values('%s','%s','%s','%s','%s')" % \
                  (collegeName, englishName, country, url, rank)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                traceback.print_exc()
                db.rollback()
            db.close()


fetchRankList(url)
