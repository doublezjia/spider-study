#
#_*_ coding: utf-8 _*_
# 爬虫学习
# 环境：python 3.x
# 目标网站：http://www.wmpic.me/tupian/yijing/
# 爬取目标地址中的图片并下载到 ./spider_pic 目录中
# 
# ver 1.0 2017-08-23
# All right reserved by zealous
# 


import sys,requests,io,re,time,os,datetime
from urllib import request
from bs4 import BeautifulSoup


# 出现乱码的时候可以用这个,encoding可以输utf8,gbk,gb2312,gb18030,big5,big5hkscs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
	}

# 文件名用数字表示
namenum = 1

# 下载图片错误数量
errnum = 0

# 爬取图片
def picspider(url):
	# 声明全局变量
	global namenum
	global errnum
	url = url
	# 获取目标网站内容，通过 BeautifulSoup进行内容筛选
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text,'html.parser')
	imgs = soup.select('#content > div.content-c ')
	# 图片地址正则
	reg = r'_cke_saved_src="(.+?\.jpg|.+?\.png|.+?\.gif)"'
	# 本地图片存放目录
	local=r'.\spider_pic\\'
	# 如果没有这个目录的就新建一个
	if not os.path.isdir(local):
		os.mkdir(local)

	# 如果获取到内容的就进行下载
	if len(imgs) > 0 : 
		# 通过正则匹配图片下载地址
		imgsrc = re.findall(reg,str(imgs[0]),re.S)
		for img in imgsrc:
			try:
				# 下载图片，以namenum命名
				request.urlretrieve(img,'%s%s.jpg' % (local,namenum))
			except UnicodeEncodeError as e:
				# 如果UnicodeEncodeError异常就把异常输出到error.log中。
				error = '[Time]'+datetime.datetime.now().strftime('%Y-%m-%d')+'\n[Error]'+str(e)+'\n[File]'+img+'\n\n'
				with open('error.log','a') as f:
					f.write(error)
				# 错误数量加1
				errnum = errnum+1
			# 名称加1
			namenum=namenum+1
	# 返回错误数量
	return errnum


# 爬取目标网站的页面地址并传到picspider()下载图片。
def pagespider(begin=1,stop=1):
	# 开始和结束页面
	begin = begin 
	stop = int(stop)+1
	for i in range(begin,stop):
		url = 'http://www.wmpic.me/tupian/yijing/page/'+str(i)
		# 获取目标网站内容
		req = requests.get(url,headers=headers)
		# 通过 BeautifulSoup进行内容筛选
		soup = BeautifulSoup(req.text,'html.parser')
		pages = soup.select('div.post > a')
		# 目标地址的正则表达式
		req = r'href="(.+?)"'
		# 补全目标地址用的
		pageurl = 'http://www.wmpic.me'
		for page in pages:
			# 通过正则匹配地址
			pagesrc = re.findall(req,str(page),re.S)
			pagesrc = pageurl+pagesrc[0]
			# 把地址传到 picspider()中
			err = picspider(pagesrc)

	# 返回错误数量
	return err


if __name__ == '__main__':
	begin = 1
	stop = 12
	err = pagespider(begin,stop)
	if err > 0 :
		print ('爬虫结束，失败'+str(err)+'个,请查看error 日志.')
	else:
		print ('爬虫结束，失败'+str(err)+'个.')