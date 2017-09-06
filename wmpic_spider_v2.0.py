#
#_*_ coding: utf-8 _*_
# 爬虫学习
# 环境：python 3.x
# 目标网站：http://www.wmpic.me/tupian/yijing/
# 爬取目标地址中的图片并下载到 ./spider_pic 目录中
# 
# 这次不用正则，只用Beautifulsoup
# 
# ver 1.0 2017-08-23
# All right reserved by zealous
# 
# 
# 

import sys,requests,io,re,time,os,datetime
from urllib import request
from bs4 import BeautifulSoup


# 出现乱码的时候可以用这个,encoding可以输utf8,gbk,gb2312,gb18030,big5,big5hkscs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


index_url = 'http://www.wmpic.me/tupian/yijing'

# 请求头
headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
	}

# 文件名用数字表示
namenum = 1
# 今天日期
today = datetime.datetime.now().strftime('%Y-%m-%d')

# 获取页面地址
def get_page_url(url):
	url = url
	# 连接页面
	req = requests.get(url,headers=headers)
	# 获取页面返回的状态码
	status_code = req.status_code
	# 如果是200表示正常访问，如果不是的就记录到日志中
	if status_code == 200 :
		# 通过 BeautifulSoup进行内容筛选
		soup = BeautifulSoup(req.text, 'html.parser')
		data = soup.find('ul', {'class': 'item_list'}).find_all('div',class_='post')
		# 补全目标地址用的
		pageurl = 'http://www.wmpic.me'
		for item in data:
			# 获取页面地址
			pagesrc=item.find('a')['href']
			pagesrc = pageurl+pagesrc
			# 传到get_img执行下一步
			get_img(pagesrc)
	else:
		logpath = r'./log'
		if not os.path.isdir(logpath):
			os.mkdir(logpath)
		error = '[Faild] Page'+pageurl+' access error. Number is '+str(status_code)+' '+today+'\n'
		errfile = logpath+'/'+'errorlog.log'
		with open(errfile,'a') as f:
			f.write(error)	


# 下载图片
def get_img(url):
	# 声明全局变量
	global namenum
	url = url
	# 连接页面并获取状态码
	req = requests.get(url,headers=headers)
	status_code = req.status_code
	if status_code == 200 :
		# 通过 BeautifulSoup进行内容筛选
		soup = BeautifulSoup(req.text,'html.parser')
		# 本地图片存放目录
		picpath=r'.\spider_pic\\'
		# 如果没有这个目录的就新建一个
		if not os.path.isdir(picpath):
			os.mkdir(picpath) 
		try:
			data = soup.find('div',{'class':'content-c'}).find_all('img')
			for item in data:
				img = item['src']
				# 下载图片
				request.urlretrieve(img,'%s%s.jpg' % (picpath,namenum))
				namenum=namenum+1
			return 0
		except AttributeError as e:
			return 1
	else:
		logpath = r'./log'
		if not os.path.isdir(logpath):
			os.mkdir(logpath)
		error = '[Faild] Page'+pageurl+' access error. Number is '+str(status_code)+' '+today+'\n'
		errfile = logpath+'/'+'errorlog.log'
		with open(errfile,'a') as f:
			f.write(error)		

# 爬取的页数
def page(begin=1,end=1):
	begin = begin
	end = end+1
	for i in range(begin,end):
		pageurl = index_url+'/page/'+str(i)
		get_page_url(pageurl)
		
	
if __name__ == '__main__':
    page(1,1)