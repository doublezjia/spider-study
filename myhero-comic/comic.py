#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-12-13 14:36:53
# @Author  : zealous (doublezjia@163.com)
# @Link    : https://github.com/doublezjia
# @Version : 1.0
# @Desc    : Comic Spider
#
# 爬虫环境：Python3.5
#
# 本爬虫是用来下载我的英雄学院的漫画
# 爬取网站为:http://manhua.fzdm.com
# 爬取的目标地址为:http://manhua.fzdm.com/131/
#
# 需要安装BeautifulSoup库和selenium库，可以通过pip安装
#
# 爬虫通过 selenium+PhantomJS 读取页面中JavaScript生成的图片地址
# 爬虫可以判断系统为Windows还是Linux,然后执行相应的PhantomJS
#
# 通过platform.system获取系统信息，判断系统
#
# PhantomJS是个无界面的浏览器。
#
# 爬取的漫画存放在以漫画名命名的文件夹中，每一话以话数为文件夹，每一页以页数为文件名
# 默认是从第一话开始,所以默认ep='01',如果默认为第一卷的请在main中添加参数 ep='Vol_001'
# 如果爬取其他漫画的请修改bash_url中的地址，如地址中的131代表的是我的英雄学院，其他的请修改相应的数字，
# 具体请观察网站本身。
# 如果要爬新的漫画请先把spider-urllist.log文件删除了，然后再运行爬虫。
#
# 文件说明：
# comic.py 爬虫脚本
# spider-urllist.log 存放爬取的页面地址，以便下次运行继续爬取
# ./phantomjs/ phantomjs的程序
# spider-log.log 日志文件
#




import requests,os,sys,time,platform
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# 防止递归深度出错 把值设置大一点
sys.setrecursionlimit(1000000) 

# 请求头
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

# cookies = {
# 	'Hm_lvt_cb51090e9c10cda176f81a7fa92c3dfc':'1512965895',
# 	'Hm_lpvt_cb51090e9c10cda176f81a7fa92c3dfc':'1512965895',
# 	'UM_distinctid':'16043cb731b604-024be7d1bde1d6-173a7640-1aeaa0-16043cb731c690',
# 	'picHost':'101.110.118.61/p1.xiaoshidi.net',
# 	'__utma':'182137712.242291461.1512965898.1512965898.1512965898.1',
# 	'__utmb':'182137712.1.10.1512965898',
# 	'__utmc':'182137712',
# 	'__utmz':'182137712.1512965898.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
# 	'__utmt':'1'
# }

# 基本的url
bash_url = 'http://manhua.fzdm.com/131/{ep}/{pageurl}'

# 这个用于存储从文本中读出的url
pagelist = []

# 漫画页面，下载漫画并跳转到下一页地址
def Comic_page(ep='01',pageurl='index_0.html'):
	url = bash_url.format(ep=ep,pageurl=pageurl)

	# 判断页面是否正常打开
	req_status = requests.get(url,headers=headers).status_code
	if req_status != 200 :
		print ('页面不能正常访问，爬虫停止')
		print ('页面状态码为：%s' % req_status)
		print ('问题页面为：%s' % url)
		print ('退出运行')
		# 保存到日志文件
		error = '[Error] Error Page: %s ,Status Code: %s \n' % (url,req_status)
		with open('spider-log.log','a') as f:
			f.write(error)
		return None

	print ('正在爬取页面地址：%s' % url)
	print ('正在获取本页漫画下载地址....')
	# 下载漫画
	# f_dir = ep
	f_name = pageurl.replace('index_','').split('.')[0]
	f_url,root_dir,f_dir = get_Comic_url(url)
	down_Comic(url=f_url,rootdir=root_dir,fdir=f_dir,fname=f_name)

	# 如果url不在列表中的
	if url not in pagelist:
		# 把已经下载的页面保存到文本中
		with open('spider-urllist.log','a') as f:
			f.write(url+'\n')

	# 获取下一页
	Comic_next_page(url,ep)

# 获取下一页的地址，如果到最后一页的就获取下一话
def Comic_next_page(url,ep):
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text,'html.parser')
	data = soup.find('div',{'class':'navigation'}).find_all('a')
	for i in data:
		if i.get_text() == '下一页':
			pageurl = i['href']
			print ('开始爬取下一页的内容....')
			return Comic_page(ep=ep,pageurl=pageurl)
		elif i.get_text() == '下一话吧':
			next_ep = i['href'].split('/')[1]

			# 这个是目标页面有问题，只能这样写判断，要是爬其他漫画应该可以注释掉
			# 这个网站的我的英雄学院的漫画页面获取有问题，42话之前的下一话都会不断的跳到42话
			# 这个网站的其他漫画应该不会
			myhero_url ='http://manhua.fzdm.com/131/'
			if myhero_url in url:
				if next_ep == '42':
					next_ep = int(ep)+1
					if next_ep < 10:
						next_ep = '0'+str(next_ep)
				elif next_ep == 'sdsg':
					next_ep = '72'

			print ('开始爬取下一话的漫画....')		
			return Comic_page(ep=str(next_ep))

# 获取下载地址
def get_Comic_url(url):
	# PhantomJS相关
	service_args=[]
	service_args.append('--load-images=no')  ##关闭图片加载
	service_args.append('--disk-cache=yes')  ##开启缓存
	service_args.append('--ignore-ssl-errors=true') ##忽略https错误

	# 关闭PhantomJS图片加载
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.loadImages"] = False

	# 通过platform.system()判断系统版本是Linux还是Windows,执行相应的PhantomJS
	if platform.system() == 'Windows':
		# 通过 selenium+PhantomJS 读取页面中JavaScript生成的图片地址
		driver = webdriver.PhantomJS('./phantomjs/phantomjs-2.1.1-windows/bin/phantomjs.exe',service_args=service_args,desired_capabilities=dcap)
	elif platform.system() == 'Linux':
		# 通过 selenium+PhantomJS 读取页面中JavaScript生成的图片地址
		driver = webdriver.PhantomJS('./phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',service_args=service_args,desired_capabilities=dcap)
	driver.get(url)

	# 匹配内容,selenium中是通过page_source读取获取到的页面内容
	soup = BeautifulSoup(driver.page_source,'html.parser')
	try:
		# 获取下载地址，漫画目录名和每一话的文件夹名
		comic_down_url = soup.find('div',{'id':'mhimg0'}).find('img')['src']
		root_dir = soup.find('div',{'id':'weizhi'}).find_all('a')[-2].get_text()
		fdir = soup.find('div',{'id':'mh'}).find('h1').get_text()
		return comic_down_url,root_dir,fdir
	except AttributeError as e:
		error = '[Error] Message: %s ,Error Page: %s \n' % (e,url)
		print ('访问出错，页面没有匹配的内容')
		with open('spider-log.log','a') as f:
			f.write(error)		
		sys.exit('退出运行')

# 下载漫画
def down_Comic(url,rootdir='file',fdir='test',fname='0'):
	f_Suffixes = url.split('.')[-1]
	root_dir = './'+rootdir
	fdir = root_dir+'/'+str(fdir)
	if not os.path.isdir(root_dir):
		os.mkdir(root_dir)
	if not os.path.isdir(fdir):
		os.mkdir(fdir)
	file =fdir+'/'+fname+'.'+f_Suffixes
	req = requests.get(url,headers=headers)
	print ('下载漫画......')
	time.sleep(1)
	with open(file,'wb') as f:
		f.write(req.content)
	print ('漫画下载完成....')
	time.sleep(1)

# 主函数
def main(ep='01'):
	# 如果没有spider-urllist.log就新建一个
	if not os.path.isfile('spider-urllist.log'):
		open('spider-urllist.log','w+').close()
	# 逐行读取spider-urllist.log中的地址
	with open('spider-urllist.log','r') as f:
		url_list = f.readlines()

	# 如果url_list不为空，则把地址添加到pagelist中，用于继续上次下载
	# 如果为空就从第一话开始下载
	if url_list:
		for url in url_list:
			pagelist.append(url.strip('\n'))
		# 获取第几话和第几页
		ep = pagelist[-1].replace('http://','').split('/')[-2]
		pageurl = pagelist[-1].replace('http://','').split('/')[-1]
		Comic_page(ep=ep,pageurl=pageurl)
	else:
		Comic_page(ep=ep)



if __name__ == '__main__':
	print ('***************** Comic Spider ******************\n')
	try:
		main()
	except KeyboardInterrupt:
		print ('退出运行')	
