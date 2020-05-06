#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : zealous (doublezjia@163.com)
# @Date    : 2020-05-06
# @Link    : https://github.com/doublezjia
# @Desc    :广东卫健委疫情最新情况


import requests
from bs4 import BeautifulSoup


import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
}

url = "http://wsjkw.gd.gov.cn/zwyw_yqxx/index.html"

def page(url):
    url = url
    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.text,'html.parser')
    data = soup.find('div',{'class':'content-content'})
    return data

def sendEmail(title,msg):
    sender = 'abc@qq.com'
    sender_pwd = 'password'
    receivers = 'abc@qq.com'
    message = MIMEText(msg,'html','utf-8')
    message['From'] = formataddr(["zealous",sender])
    message['TO'] = formataddr(["zealous",receivers])
    message['Subject'] = title
    server = smtplib.SMTP_SSL('smtp.qq.com',465)
    server.login(sender,sender_pwd)
    server.sendmail(sender,[receivers,],message.as_string())

def main():
    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.text,'html.parser')
    data = soup.find('div',{"class":'section list'}).find('ul').find_all('li')
    page_url = data[0].a['href']
    title = data[0].a['title']
    content = page(page_url)
    try:
        sendEmail(title,content)
        print ('SEND EMAIL SUCCESSFULLY.')
    except:
        print ('error')

if __name__ == "__main__":
    main()
