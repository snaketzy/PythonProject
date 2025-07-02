from splinter import Browser
import time
from urllib import request
from urllib import parse
import string
import json
from bs4 import BeautifulSoup
import re
import traceback
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header


url = 'https://hdhome.org'
urlCheckIn = 'http://hdhome.org/torrents.php?cat450=1&cat499=1&cat451=1&cat500=1&incldead=1&spstate=0&inclbookmarked=0&search=&search_area=0&search_mode=0'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
    "cookie": "__cfduid=d920b0941d5bceb5c2ae96cf8f09bf9661529474621; __cfduid=d62c67249fcaed37080ede9d7a933c5cf1529470692; c_secure_login=bm9wZQ%3D%3D; c_secure_pass=de169a78693d815b7fc014a2ef23130c; c_secure_ssl=bm9wZQ%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_uid=MTAxMzAy"
}





def sendMail(content):
    # 第三方 SMTP 服务,qq
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "12961606@qq.com"  # 用户名
    mail_pass = "fbgnjlisgmsxbhag"  # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格

    sender = '12961606@qq.com'
    # receivers = 'tangzy@viphrm.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    receivers = 'snaketzy@163.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # message = MIMEText('a test for python@'+time.strftime('%Y-%m-%d %H:%M:%S'), 'plain', 'utf-8')
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("Jerry Tang <"+sender+">", 'utf-8')
    message['To'] = Header("Jerry Tang <"+receivers+">", 'utf-8')
    subject = 'HDHome update@'+time.strftime('%Y-%m-%d %H:%M:%S')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.ehlo()
        # smtpObj.starttls()
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("error")
        traceback.print_exc()

def getFreeRecord(urlCheckIn):
    recordList = ''
    urlRequest = request.Request(url=urlCheckIn,headers=headers)
    response = request.urlopen(urlRequest).read()
    data = BeautifulSoup(response.decode("utf-8"),"html.parser")
    records = data.find_all("table",class_="torrentname")
    for index,record in enumerate(records):
        freeRecord = record.find_all("img",class_="pro_free")
        if freeRecord.__len__()!=0:
            # print(record.getText().strip())
            # print(record.find("a").get("href")+"\n")
            # recordList + record.getText().strip()+"\n"
            recordList = recordList + record.getText().strip() + "\n\n"
    print(recordList+"\n")
    # sendMail(recordList)

while True:
    getFreeRecord(urlCheckIn)
    time.sleep(1800)
# sendMail()