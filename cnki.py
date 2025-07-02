# 运行本程序前，请确定基础环境为python 3 以上，另外import的各依赖库都已安装。

# import requests
# import xml.etree.ElementTree as ET
# from xml.parsers.expat import ParserCreate
#
#
import re
import urllib3
from urllib3 import encode_multipart_formdata

import urllib
import requests
from urllib import request
from urllib.parse import quote
import time
import urllib.parse as urlparse
import string
from bs4 import BeautifulSoup
import pymysql
import traceback
import json

# 爬取数据的列表起始页
globalIndex = 1;


needNumber = 15;
preferPageSize = 50;
# 需要爬到多少页
preferNumber = globalIndex + needNumber;

# 知网用来做用户鉴权的凭证，登录以后获取，已知规律是抓取16页后会被强制中止，需要重新获取
globalCookie = 'RsPerPage=20; cnkiUserKey=407da644-9f75-b2bd-d206-3b50419d851f; ASP.NET_SessionId=jsnzzqvqxg4zwrjsmgso1i3u; Hm_lvt_7ad0e218cfd89a6bcabf4ce749d7c3db=1617209774,1617210867; CurrSortField=%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2f(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27TIME%27); CurrSortFieldType=desc; SID=013009; _pk_id=09c3a550-553e-43ce-99e0-f8784ec64988.1619393081.2.1619444073.1619444020.; __LastReferenceId=a20f38c959; Ecp_IpLoginFail=210428218.82.68.151; Ecp_ClientId=4489162012a940fa; LID=WEEvREcwSlJHSldTTEYzVDhUQ05aYTl2UlpVOERFRjB5UXdLNmZrWlRpUT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!; Hm_lpvt_7ad0e218cfd89a6bcabf4ce749d7c3db=1619560831; c_m_expire=2021-4-29 6:03:02; c_m_LinID=LinID=WEEvREcwSlJHSldTTEYzVDhUQ05aYTl2UlpVOERFRjB5UXdLNmZrWlRpUT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!&ot=2021-4-29 6:03:02; Ecp_LoginStuts={"UserName":"13611885280","ShowName":"13611885280","IsAutoLogin":false,"UserType":"jf","r":"35e60a"}'


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": globalCookie,
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}


# 对列表页的每条连接获取详细数据
def getDetail(querys):
    # url1 = urllib.parse.unquote(url1, encoding='utf-8', errors='replace')
    # fp = request.urlopen(quote(url1, safe='/:?=')).read()
    # data = BeautifulSoup(fp.decode("utf-8"), "html.parser")

    # 知网专门提供了一个api。用于获取论文的所有数据，只能通过接口的post方式访问
    url = "https://x.cnki.net/read/LitNotes/GetPaperInfo";
    FileName = querys.get("filename")
    DbName = querys.get("dbCode") or query.get("DbCode")


    data = {
        "fileName" : "".join(FileName),
        "dbCode": "".join(DbName)
    }
    # data = '{"fileName":'+ querys["FileName"] +',"tableName":"CJFDTOTAL","dbCode":'+ querys["DbCode"] +',"from":"","type":"psmc","fsType":"1","taskId":"0"}'

    headersNew = {
        "Cookie": globalCookie,
        'Content-Type':"application/x-www-form-urlencoded"
        # 'Content-Type':"application/form-data"
    }
    # headersNew['Content-Type'] = "multipart/form-data"

    response = requests.request(method='post', url=url, data=urllib.parse.urlencode(data), headers=headersNew)
    result = json.loads(response.text)
    # time.sleep(1)
    if(result["Data"]):
        dataResult = result["Data"];
        for index, item in enumerate(dataResult):

           if(item == "Paper"):
               print("".join(dataResult[item].get("Title")))
               fp.write("中文标题："+ "".join(dataResult[item].get("Title"))+"\n")

               if(dataResult[item].get("EnglishTitle")):
                    fp.write("英文标题："+ "".join(dataResult[item].get("EnglishTitle"))+"\n")
               else:
                   fp.write("英文标题：" + "\n")

               if (dataResult[item].get("Abstract")):
                    fp.write("中文摘要："+ "".join(dataResult[item].get("Abstract"))+"\n")
               else:
                    fp.write("中文摘要：" + "\n")

               if(dataResult[item].get("EnglishAbstract")):
                    fp.write("英文摘要："+ "".join(dataResult[item].get("EnglishAbstract"))+"\n")
               else:
                    fp.write("英文摘要：" + "\n")

               if (dataResult[item].get("Keywords")):
                   fp.write("中文关键词：" + "".join(dataResult[item].get("Keywords")) + "\n")
               else:
                   fp.write("中文关键词：" + "\n")

               if(dataResult[item].get("EnglishKeywords")):
                    fp.write("英文关键词："+ "".join(dataResult[item].get("EnglishKeywords"))+"\n")
               else:
                    fp.write("英文关键词：" + "\n")


               if(dataResult[item].get("SourceTitle")):
                    fp.write("期刊名称："+ "".join(dataResult[item].get("SourceTitle"))+"\n")
               else:
                    fp.write("期刊名称：" + "\n")

               if (dataResult[item].get("SourceTitleEN")):
                   fp.write("期刊名称（英文）：" + "".join(dataResult[item].get("SourceTitleEN")) + "\n")
               else:
                   fp.write("期刊名称（英文）：" + "\n")

               if (dataResult[item].get("TiluInfo")):
                   tiluInfo = json.loads(dataResult[item].get("TiluInfo"))
                   for index, item in enumerate(tiluInfo):
                       if(item == "Author"):
                           fp.write("作者：" + tiluInfo[item].__str__() + "\n")
                       if(item == "Year"):
                           fp.write("发表年份：" + tiluInfo[item].__str__() + "\n")
                       if(item == "AuthorAffiliation"):
                           fp.write("作者单位：" + tiluInfo[item].__str__() + "\n")

               fp.write("\n")
               fp.write("\n")
           # print(result)

# 对列表页的每条pdf连接获取详细数据
def getPDFDetail(querys):
    # 知网专门提供了一个api。用于获取论文的所有数据，只能通过接口的post方式访问
    url = "https://x.cnki.net/read/File/GetPdfTiluInfo";
    FileName = querys.get("FileName")
    DbName = querys.get("DbName")
    DbCode = query.get("DbCode")
    fsType = 1


    data = {
        "fileName" : "".join(FileName),
        "dbCode": "".join(DbCode),
        "fsType": "1"

    }
    # data = '{"fileName":'+ querys["FileName"] +',"tableName":"CJFDTOTAL","dbCode":'+ querys["DbCode"] +',"from":"","type":"psmc","fsType":"1","taskId":"0"}'

    headersNew = {
        "Cookie": globalCookie,
        'Content-Type':"application/x-www-form-urlencoded"
    }
    # headersNew['Content-Type'] = "multipart/form-data"

    response = requests.request(method='post', url=url, data=urllib.parse.urlencode(data), headers=headersNew)
    result = json.loads(response.text)
    # time.sleep(1)
    if(result["Data"]):
        dataResult = result["Data"];
        for index, item in enumerate(dataResult):

           if(item == "tilu"):
               print("PDF:","".join(dataResult[item].get("Title")))
               fp.write("PDF中文标题："+ "".join(dataResult[item].get("Title"))+"\n")

               if (dataResult[item].get("Summary")):
                    fp.write("PDF中文摘要："+ "".join(dataResult[item].get("Summary"))+"\n")
               else:
                    fp.write("PDF中文摘要：" + "\n")

               if (dataResult[item].get("KeyWord")):
                   fp.write("PDF中文关键词：" + "".join(dataResult[item].get("KeyWord")) + "\n")
               else:
                   fp.write("PDF中文关键词：" + "\n")

               if(dataResult[item].get("Source")):
                    fp.write("PDF期刊名称："+ "".join(dataResult[item].get("Source"))+"\n")
               else:
                    fp.write("PDF期刊名称：" + "\n")

               if (dataResult[item].get("Author")):
                   fp.write("作者：" + "".join(dataResult[item].get("Author")) + "\n")
               else:
                   fp.write("作者：" + "\n")

               if (dataResult[item].get("PubDate")):
                   fp.write("发布日期：" + "".join(dataResult[item].get("PubDate")) + "\n")
               else:
                   fp.write("发布日期：" + "\n")

               if (dataResult[item].get("ResourceType")):
                   fp.write("资源类型：" + "".join(dataResult[item].get("ResourceType")) + "\n")
               else:
                   fp.write("资源类型：" + "\n")

               if (dataResult[item].get("DOI")):
                   fp.write("DOI：" + "".join(dataResult[item].get("DOI")) + "\n")
               else:
                   fp.write("DOI：" + "\n")


               fp.write("\n")
               fp.write("\n")
           # print(result)



# 自己定义的对多少页数据进行处理
# '+ globalIndex.__str__() +'
# '+ preferPageSize.__str__()  +'
# url = 'https://x.cnki.net/kns/brief/brief.aspx?curpage='+ globalIndex.__str__() +'&RecordsPerPage='+ preferPageSize.__str__()  +'&QueryID=1&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx'

while globalIndex <= preferNumber:
    url = 'https://x.cnki.net/kns/brief/brief.aspx?curpage='+ globalIndex.__str__() +'&RecordsPerPage=50&QueryID=65&ID=&turnpage=1&tpagemode=L&dbPrefix=CJFQ&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx'

    urlRequest = request.Request(url=url,headers=headers)
    # time.sleep(1)
    response = request.urlopen(urlRequest).read()
    # time.sleep(1)


    data = BeautifulSoup(response.decode("utf-8"),"html.parser")


    linkData = data.findAll("a",{"class":"fz14"});
    if(linkData.__len__() == 0 ):
        print(globalIndex.__str__()+" 无数据")

    if (linkData.__len__() > 0):
        # 获取到数据后保存到文件
        fp = open('./article'+ globalIndex.__str__() +'.txt', 'w+',encoding="utf-8")
        print("\n")
        print(url + "\n")
        fp.write(url + "\n\n")


        for index, link in enumerate(linkData):
            parsed = urlparse.urlparse(link.get("href"))
            query = urlparse.parse_qs(parsed.query)
            querys = {k: v[0] for k, v in query.items()}

            if(querys.get("domain")):
                fp.write((index+1).__str__() + "\n")
                getDetail(urlparse.parse_qs(querys["domain"]))
            else:
                if(querys.get("FileName")):
                    fp.write((index + 1).__str__() + "\n")
                    getPDFDetail(querys)
                else:
                    fp.write((index + 1).__str__() + "\n")
                    getDetail(querys)


        fp.close()
    globalIndex = globalIndex + 1;

# print(data)
