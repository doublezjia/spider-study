#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : zealous (doublezjia@163.com)
# @Date    : 2020-04-24
# @Link    : https://github.com/doublezjia
# @Desc    : 爬取每天广州卫健委官网上发布的最新疫情情况并发送到邮箱

import requests
from bs4 import BeautifulSoup


import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
}

url = "http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/index.html"

def page(url):
    url = url
    req = requests.get(url,headers=headers)
    soup = BeautifulSoup(req.text,'html.parser')
    data = soup.find('div',{'class':'zoom_box'}).find_all('p')
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
    data = soup.find('div',{"class":'cont_list'}).find('ul').find_all('div',{'class':'title'})
    title = data[1].a['title']
    page_url = data[1].a['href']
    content = page(page_url)
    msg = ''
    for i in content:
        if not i.text == '附件：':
            msg = msg + '<p>' + i.text + '</p>'
    try:
        sendEmail(title,msg)
        print ('SEND EMAIL SUCCESSFULLY.')
    except:
        print ('error')

if __name__ == "__main__":
    main()
