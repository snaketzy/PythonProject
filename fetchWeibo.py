from splinter import Browser #自动化测试框架
import time
from urllib import request #网络请求
from urllib import parse
import string #字符串操作
import json
from bs4 import BeautifulSoup #爬虫用
import re #正则


url = 'https://weibo.com/shgjj12329?refer_flag=1001030102_&is_hot=1#_rnd1530329599558'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
    "cookie": "SINAGLOBAL=8159053886607.719.1504021939043; UM_distinctid=1633ffd030b0-076c8fe8b33c6f-33617106-fa000-1633ffd030f27e; _s_tentry=www.shzhzy.com; Apache=6654736457514.647.1529841135251; ULV=1529841135318:8:1:1:6654736457514.647.1529841135251:1525698304659; YF-Page-G0=5c7144e56a57a456abed1d1511ad79e8; UOR=play.163.com,widget.weibo.com,www.baidu.com; YF-Ugrow-G0=56862bac2f6bf97368b95873bc687eef; YF-V5-G0=731b77772529a1f49eac82a9d2c2957f; WBtopGlobal_register_version=2e7679c973813872; SCF=AsIz23sX3iHce1OMtIeHwMY8VrDOCv99rJzmAhkO-dY0ly911lsnptp9ts60Wh8ul8kSRJE4sXrag6X1sFkFmHE.; SUB=_2A252Mu3SDeRhGedI6VET8ijFzzyIHXVVRlgarDV8PUNbmtBeLXPFkW9NV9UuAHhISKKdf4sJ7DPCQg3Qsh5yZ-jd; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWlikWgWBEYqmITibzs6_305JpX5K2hUgL.Fo2ceoeEeoq4Sh52dJLoIpjLxKqLBo2LBKBLxK-L1KeLBozLxKqL1K.L1KBt; SUHB=09PMu-Po2m9rhQ; ALF=1530910722; SSOLoginState=1530305923; un=13611885280; wb_view_log_1623226940=1280*8002"
}
testString = "<p style=\"font-size:12px\"><p>"

urlRequest = request.Request(url=url,headers=headers)
response = request.urlopen(urlRequest).read()
data = BeautifulSoup(response.decode("utf-8"),"html.parser")
htmlData = data.find_all("script")
for data in htmlData:
    if data.getText().find("WB_detail")!= -1:
        filterHTML = eval(data.getText()[8:len(data.getText())-1])["html"]
        tweets = BeautifulSoup(filterHTML.replace("\\",""),"html.parser").find_all("div",class_="WB_detail")

        for index,tweet in enumerate(tweets):
            tweetMedias = tweet.find_all("div",class_="WB_media_wrap")
            #正文主体
            we_text = tweet.find("div",class_="WB_text")

            for index,text in enumerate(we_text):
                #a代表链接，img代表表情符号
                if text.name!="a" and text.name!="img":
                    print("标题："+str.strip(text))
                if text.name == "img":
                    rePattern = re.compile('</?\w+[^>]*>')
                    # rePattern.sub("",str(text))
                    # print("正文："+rePattern.sub("",str(text)))
            # print(we_text.contents)
            # print(tweet.find("div",class_="WB_text"))
            for index, tweetMedia in enumerate(tweetMedias):
                print("图片："+str(tweetMedia.find_all("img")[0]))
            print("\n")

