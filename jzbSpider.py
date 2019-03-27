import re
import urllib3
import os
from urllib import request
from urllib.parse import quote
import string
import json
import pymysql
from bs4 import BeautifulSoup
import traceback



url1 = "http://www.jzb.com/bbs/forum-1137-1.html"

fp = request.urlopen(url1).read()
data = BeautifulSoup(fp.decode("utf-8"),"html.parser")
dataContent = data.find_all("span",attrs={"class":"xst thread-name"})
pg = data.find("a",attrs={"class":"last"})

startIndex = 1
endIndex = re.sub("\... ",'',pg.get_text())
currentIndex = 1
urls = []

# 循环拿到本栏目下的分页url
# while currentIndex <= int(endIndex):
while currentIndex <= 1:
    urls.append("http://www.jzb.com/bbs/forum-1137-"+str(currentIndex)+".html")
    currentIndex += 1


# 获得页面dom数据
def getContent(url):
    fp = request.urlopen(url).read()
    data = BeautifulSoup(fp.decode("utf-8"), "html.parser")
    return data

# 循环拿到本帖的分页url
def getArticlePages(url,dom,type):
    # articlePg = dom.find("a", attrs={"class": "last"})
    templateUrl = re.sub("\-1-1.html",'',url)
    totalPages = dom.select("span[title*='共']")
    if len(totalPages) > 0:
        articlePg = re.sub("\/|\页|\ ", '', totalPages[0].get_text())
        articleStartIndex = 1
        # articleEndIndex = re.sub("\... ", '', articlePg.get_text())
        articleEndIndex = articlePg
        articleCurrentIndex = 1
        articleUrls = []
        while articleCurrentIndex <= int(articleEndIndex):
            articleUrls.append(templateUrl + "-" + str(articleCurrentIndex) + "-1.html")
            articleCurrentIndex += 1
        return articleUrls
    else:
        return [templateUrl+"-1-1.html"]

# 拿到文章下的每个comment，并将数据写入数据库
def fetchArticleComment(data,href,page):
    comments = data.find_all("div",attrs={"class":"eduu_brg eduu_thread_Box","style":""})
    for comment in comments:
        # comment类型
        if comment.find("div",attrs={"class":"eduu_floor_One"}):
            articleCommentType = 1
            print("comment类型：主楼")
        else:
            articleCommentType = 2
            print("comment类型：跟帖")

        # comment作者
        if comment.find("a",attrs={"class":"xw1 Tt_ifo_name"}):
            articleCommentAuthor = comment.find("a", attrs={"class": "xw1 Tt_ifo_name"}).get_text()
            print(articleCommentAuthor)
        else:
            print("无作者")

        # comment作者Id
        if comment.find("a", attrs={"class": "xw1 Tt_ifo_name"}):
            articleCommentAuthorId = int(re.sub("thread-|-1-1|.html","",comment.find("a",attrs={"class":"xw1 Tt_ifo_name"}).get("href")).split("-")[1])
        else:
            print("无作者Id")
        #comment发表时间
        if comment.find("div", attrs={"class": "eduu_floor_One"}):
            articleCommentPostDate = comment.find("em",attrs={"class":"y eduu_c9"}).find("em").get_text()
        else:
            if comment.find("div",attrs={"class":"eduu_rept_rt"}):
                articleCommentPostDate = comment.find("div", attrs={"class": "eduu_rept_rt"}).find("em").get_text()
            else:
                articleCommentPostDate = "无日期"
        # comment内容
        if comment.find("td",attrs={"class":"t_f"}):
            articleCommentContent = comment.find("td",attrs={"class":"t_f"}).get_text()
        else:
            articleCommentContent = "作者被禁止或删除 内容自动屏蔽"
        # comment对应url
        articleCommentUrl = page
        print("comment对应url："+articleCommentUrl)
        # comment归属贴id
        articleId = int(re.sub("thread|-1-1|.html","",href).split("-")[1])



        # 操作数据库
        # print("操作数据库")

# 下载进度计算
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

# 家长帮论坛日期计算
def latestReplyDate(ReplyString):
    print(ReplyString)


# 拿到本栏目所有文章数据
# 根据urls列表来做循环

db = pymysql.connect("localhost", "root", "snaketzy123$","education")
for url in urls:
    # 拿到当前url的dom
    dataContent = getContent(url)
    content = dataContent.find_all("span", attrs={"class": "xst thread-name"})
    for items in range(2):
        cursor = db.cursor()
        href = content[items].find("a",title=True).get("href")
        title = content[items].find("a",title=True).get("title")
        by = content[items].find_parent().find_next_sibling()
        replies = int(content[items].find_parent().find_next_sibling().find_next_sibling().find("a").get_text())
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print("Database version : %s " % data)
        print("本列表页的url为："+ url)
        print("本贴的标题为：" + title)
        print("本贴的链接为："+ href)
        print("本贴的回复数为："+ str(replies))
        articlePages = getArticlePages(href,getContent(href),"article")

        # print("本贴的url有："+str(articlePages))

        # 拿到贴子每页的dom结构，然后获取comment的数据
        for page in articlePages:
            pageContent = getContent(page)
            fetchArticleComment(pageContent,href,page)
        print("\n")

db.close()
# jsonData = json.loads(dataContent)

# print(dataContent)
# print(os.getcwd())
# if(os.path.exists(os.getcwd()+"/"+data.title.get_text())):
#     print("目录已存在")
# else:
#     # os.makedirs(os.getcwd()+"/"+data.title.get_text())
#     print("目录为新")
# print("\n")

# print(data.title.get_text())
# print(urls)



# for items in dataContent:
#     print(items.find("a").get("title"))
#     print(items.find("a").get("href"))


# 打开数据库连接

# localhost 为 本地连接
# root 为用户名
# password 为密码
# test_data 为数据库
# db = pymysql.connect("localhost", "root", "snaketzy123$","education")

# 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()

# print("Database version : %s " % data)

# 关闭数据库连接
# db.close()