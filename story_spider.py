#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-12-20 14:23:58
# @Author  : zealous (doublezjia@163.com)
# @Link    : https://github.com/doublezjia
# @Version : $Id$
# @Desc    : 

# 获取网站的小说并下载
# 目标地址：http://www.211zw.com/html/422/422155/38248805.shtml
# 因为这个网站的原因，所以通过判断下一章是否为章节列表就可以判断是否到最后一章了。


import os,sys,io,requests,re,time
from bs4 import BeautifulSoup

# 每一章基本页面地址
bash_url = 'http://www.211zw.com/html/422/422155/{chapter_page}'

# 第一章
begin_url = 'http://www.211zw.com/html/422/422155/38248805.shtml'

# 章节列表
list_url = 'http://www.211zw.com/html/422/422155/0.shtml'

# 请求头
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}


# 获取网页
def req_page(url):
	req = requests.get(url,headers=headers)
	# 网站是gbk码,所以要转换
	req.encoding='gbk'
	# 如果连接正常就返回内容
	if req.status_code == 200 :
		return req.text
	else:
		print ('连接网站出错，错误代码为：%s' % req.status_code)

# 获取内容
def chapter(reqpage):
	print ('获取网站内容。。。。')
	soup = BeautifulSoup(reqpage,'html.parser')
	# 获取文章标题
	title = soup.find('div',{'class','title'}).find('h1').get_text().replace('正文','').strip()
	# 获取正文
	content = soup.find('div',{'id':'content'}).get_text()
	# 清除网页中的&nbsp; 对应的gbk码为\xa0
	cont = content.replace('\xa0','')
	print ('正在下载[ %s ]的内容' % title)
	# 下载小说
	cont_down(cont,title)
	
	print ('开始下一章')
	# 防止爬虫太快
	time.sleep(1)

# 获取下一页地址
def next_chapter_url(reqpage):
	soup = BeautifulSoup(reqpage,'html.parser')
	# 获取下一页地址
	data = soup.find('div',{'class':'jump'}).find_all('a')
	for i in data:
		if i.get_text() == '下一章>>':
			chap = i['href'].split('/')[-1]
			url = bash_url.format(chapter_page=chap)
			return url

# 下载小说
def cont_down(content,fname):
	# 通过正则清除HTML编码
	dr = re.compile(r'<[^>]+>',re.S)
	cont = dr.sub('',content)

	# 把文件存放在file中,以文件章节命名
	fdir = './file'
	if not os.path.isdir(fdir):
		os.mkdir(fdir)
	file = fdir+'/'+fname+'.txt'
	with open(file,'w') as f:
		f.write(cont)
	print ('下载完成')

# 主函数
def main():
	# 第一页
	url = begin_url
	# 设置循环
	while True:
		# 如果等于这个地址就退出运行
		if url == list_url:
			print ('已经爬取完成，文件在file目录中')
			sys.exit('退出运行')
		else:
			# 获取网页
			reqpage = req_page(url)
			# 获取内容
			try:
				chapter(reqpage)
			except :
				print (url)
			# 获取下一页地址
			url = next_chapter_url(reqpage)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print ('停止运行')

