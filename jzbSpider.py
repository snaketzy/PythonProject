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
import datetime


url1 = "http://www.jzb.com/bbs/forum-1137-1.html"

fp = request.urlopen(url1).read()
data = BeautifulSoup(fp.decode("utf-8"),"html.parser")
dataContent = data.find_all("span",attrs={"class":"xst thread-name"})
pg = data.find("a",attrs={"class":"last"})

startIndex = 1
endIndex = re.sub("\... ",'',pg.get_text())
# currentIndex = 1
# currentIndex = 100
# currentIndex = 200
# currentIndex = 500
# currentIndex = 1000
# currentIndex = 1001
# currentIndex = 1137
# currentIndex = 108
# currentIndex = 109
# currentIndex = 111
"""
currentIndex = 159 - 213
"""
# currentIndex = 214
currentIndex = 240
urls = []

# 循环拿到本栏目下的分页url
while currentIndex <= int(endIndex):
# while currentIndex <= 1:
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

"""
字符串转日期
"""
def str2date(str,date_format="%Y-%m-%d %H:%M"):
    date = datetime.datetime.strptime(str, date_format)
    return date

# 连接数据库
# db = pymysql.connect("localhost", "root", "snaketzy123$","education")
db = pymysql.connect("localhost", "root", "root","education")

"""
加入本贴内容到jzb_article表
@param poster 发贴人
@param postDate 发贴日期
@param title article标题
@param href article对应的url
@param viewed article的浏览数
@param replies article的回复数
@param articlePages article的页数
"""
def insertArticle(poster,postDate,title,href,viewed,replies,articlePages):
    fetchUrl = "select * from jzb_article where articleUrl = \""+href+"\" and reply = "+str(replies)+""
    cursor.execute(fetchUrl)
    result = cursor.fetchall().__len__()

    if result > 0:
        print("数据库中已有acritle")
    else:
        sql =  "insert into jzb_article(author,postDate,articleName,articleUrl,viewed,reply,articleDetailPages)\
                      values('%s','%s','%s','%s','%s','%s','%s')" % \
                      (poster,postDate,title,href,viewed,replies,articlePages)
        try:
            cursor.execute(sql)
            # print("")
            db.commit()
        except:
            traceback.print_exc()
            db.rollback()

"""
贴子是否已存在
@param href 主题帖的url
@param replies 主题帖的回复量
"""
def articleIsExist(href,replies):
    fetchUrl = "select * from jzb_article where articleUrl = \"" + href + "\" and reply = " + str(replies) + ""
    cursor.execute(fetchUrl)
    result = cursor.fetchall().__len__()
    return result

"""
校验articleComment数量
@param href 主题帖的url
@param replies 主题帖的回复量
"""
def articheCommentIsMatch(href):
    fetchUrl = "select * from jzb_articlecomment where articleCommentArticleUrl = \"" + href + "\""
    cursor.execute(fetchUrl)
    result = cursor.fetchall().__len__()
    return result

"""
加入本comment内容到jzb_articlecomment表
@param href comment归属贴url
@param articleCommentUrl comment对应url
@param articleId comment归属贴id
@param articleCommentType comment类型
@param articleCommentAuthor  comment作者
@param articleCommentAuthorId comment作者Id
@param articleCommentPostDate comment发表时间
@param articleCommentContent comment内容
@param articleCommentFloor comment第几楼
"""
def insertArticleComment(href,articleCommentUrl,articleId,articleCommentType,articleCommentAuthor,articleCommentAuthorId,articleCommentPostDate,articleCommentContent,articleCommentFloor):
    # """
    # 先更新现有旧数据，然后转insert逻辑
    # """
    # cursor.execute(
    #     "select * from jzb_articlecomment where articleCommentAuthor = \"" + articleCommentAuthor + "\" and articleCommentPostDate = \"" + articleCommentPostDate + "\" and ISNULL(articleCommentFloor)")
    # result = cursor.fetchall().__len__()
    # if result > 0:
    #     cursor.execute("update jzb_articlecomment set jzb_articlecomment.articleCommentFloor = \"" +articleCommentFloor+ "\" where jzb_articlecomment.articleCommentId in (select * from jzb_articlecomment where articleCommentAuthor = \"" + articleCommentAuthor + "\" and articleCommentPostDate = \"" + articleCommentPostDate + "\" and articleCommentFloor = \"\") ")
    # else:
    #     print("旧数据更新完成")




    cursor.execute("select * from jzb_articlecomment where articleCommentAuthor = \"" + articleCommentAuthor + "\" and articleCommentPostDate = \"" + articleCommentPostDate + "\"")
    # cursor.execute("select * from jzb_articlecomment where articleCommentAuthor = \"" + articleCommentAuthor + "\" and articleCommentPostDate = \"" + articleCommentPostDate + "\" and articleCommentFloor = \"" + articleCommentFloor + "\"")
    result = cursor.fetchall().__len__()

    if result > 0:
        print("数据库中已有acritleComment")
    else:
        sql = "insert into jzb_articlecomment(articleCommentArticleUrl,articleCommentArticlePage,articleId,articleCommentType,articleCommentAuthor,articleCommentAuthorId,articleCommentContent,articleCommentPostDate)\
                          values('%s','%s','%s','%s','%s','%s','%s','%s')" % \
              (href,
               articleCommentUrl,
               articleId,
               articleCommentType,
               articleCommentAuthor,
               articleCommentAuthorId,
               articleCommentContent,
               articleCommentPostDate
               )
        try:
            cursor.execute(sql)
            # print("")
            db.commit()
        except:
            traceback.print_exc()
            db.rollback()

"""
拿到文章下的每个comment，并将数据写入数据库
@param data 传入的dom结构
@param href 归属于哪个article
@param page 当前第几个page
"""
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
            articleCommentAuthor = "无作者"
            print("无作者")

        # comment作者Id
        if comment.find("a", attrs={"class": "xw1 Tt_ifo_name"}):
            articleCommentAuthorId = int(re.sub("thread-|-1-1|.html","",comment.find("a",attrs={"class":"xw1 Tt_ifo_name"}).get("href")).split("-")[1])
        else:
            articleCommentAuthorId = "无作者Id"
        # comment发表时间
        if comment.find("div", attrs={"class": "eduu_floor_One"}):
            articleCommentPostDate = comment.find("em",attrs={"class":"y eduu_c9"}).find("em").get_text()
        else:
            if comment.find("div",attrs={"class":"eduu_rept_rt"}):
                articleCommentPostDate = comment.find("div", attrs={"class": "eduu_rept_rt"}).find("em").get_text()
            else:
                articleCommentPostDate = "无日期"
        # comment 楼层
        if comment.find("div", attrs={"class": "eduu_floor_One"}):
            articleCommentFloor = "1"
        else:
            if comment.find("div",attrs={"class":"eduu_rept_rt"}):
                articleCommentFloor = comment.find("div", attrs={"class": "eduu_rept_rt"}).find("strong").find("em").get_text()
            else:
                articleCommentFloor = "null"
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

        """
        操作数据库
        @param href comment归属贴url
        @param articleCommentUrl comment对应url
        @param articleId comment归属贴id
        @param articleCommentType comment类型
        @param articleCommentAuthor  comment作者
        @param articleCommentAuthorId comment作者Id
        @param articleCommentPostDate comment发表时间
        @param articleCommentContent comment内容
        """
        insertArticleComment(
            href,
            articleCommentUrl,
            articleId,
            articleCommentType,
            articleCommentAuthor,
            articleCommentAuthorId,
            articleCommentPostDate,
            articleCommentContent,
            articleCommentFloor
        )



# 拿到本栏目所有文章数据
# 根据urls列表来做循环
for url in urls:
    # 拿到当前url的dom
    dataContent = getContent(url)
    content = dataContent.find_all("span", attrs={"class": "xst thread-name"})
    # for items in range(2):
    for items in content:
        cursor = db.cursor()
        # 贴链接
        href = items.find("a",title=True).get("href")
        # 贴标题
        title = items.find("a",title=True).get("title")
        # 发帖人
        by = items.find_parent().find_next_sibling()
        poster = by.find("cite").find("a").get_text()
        # 发贴日期
        postDate = by.find("em").find("span").get_text()
        # 贴浏览数
        viewed = int(items.find_parent().find_next_sibling().find_next_sibling().find("em").get_text())
        # 贴回复数
        replies = int(items.find_parent().find_next_sibling().find_next_sibling().find("a").get_text())

        # cursor.execute("SELECT VERSION()")
        # data = cursor.fetchone()
        # print("Database version : %s " % data)

        print("本列表页的url为："+ url)
        print("本贴的标题为：" + title)
        print("本贴的链接为："+ href)
        print("本贴的回复数为："+ str(replies))
        articlePages = getArticlePages(href,getContent(href),"article")

        articleChange = articleIsExist(href, replies)
        articleCommentMatch = articheCommentIsMatch(href)

        if articleChange == 0:
            # 数据入库
            insertArticle(poster, postDate, title, href, viewed, replies, articlePages.__len__())
            # print("本贴的url有："+str(articlePages))
            # 拿到贴子每页的dom结构，然后获取comment的数据
            for page in articlePages:
                pageContent = getContent(page)
                fetchArticleComment(pageContent, href, page)
            print("\n")
        else:
            print("本帖未发生变化,不做insertArticle操作")
            """
            就算已经有了article，因为各种原因，可能丢失comment，因此要对comment和replies的数量匹配进行校验，
            以确定是否需要更新comment
            """
            if replies == articleCommentMatch:
                print("本帖回复数匹配，不做insertArticleComment操作")
            else:
                for page in articlePages:
                    pageContent = getContent(page)
                    fetchArticleComment(pageContent, href, page)
                print("\n")
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