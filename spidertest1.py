#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from urllib import request
import re,os

pages = []
cont = {}
def getUrl(url):
    myUrl = url
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
    headers = { 'User-Agent' : user_agent }   
    req = request.Request(myUrl, headers = headers)   
    myResponse = request.urlopen(req)  
    myPage = myResponse.read()
    unicodePage = myPage.decode('utf-8')
    return unicodePage

def getPage(purl):
    req = '<li><a href="(/article/.+?)" target="_blank">(.+?)</a></li>'
    pages = re.findall(req,getUrl(purl),re.S)
    return pages

def getContent(purl):
    titlereq = '<title>(.+?) - 廖雪峰的官方网站</title>'
    contentreq = '<div class="x-article-content">(.+?)</div>'
    title = re.findall(titlereq,getUrl(purl),re.S)
    content = re.findall(contentreq,getUrl(purl),re.S)
    cont = {title[0]:content[0]}
    return cont



print ('''
------------------------------------------
爬虫测试：
网站：http://www.liaoxuefeng.com
------------------------------------------
''')
print ('正在运行---------------')
item = getPage('http://www.liaoxuefeng.com')
#~ print (item)
#~ exit()
for i in range(len(item)+1):
    txt = item[i][1]+'.txt';
    purl = 'http://www.liaoxuefeng.com'+item[i][0];
    con = getContent(purl)
    for k,v in con.items():
        try:
            with open(txt,'a') as f:
                a = k+'\n'+v
                f.write(a)
        except:
            print ('Error!!!!!!')
            exit()
    if i == len(item):
        print ('OK!!!!!!!!')
        break;
