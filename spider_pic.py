#!/usr/bin/env python3
#_*_ coding: utf-8 _*_
#
#Spider_site:http://www.ivsky.com/bizhi/index_1.html
#The Spider is Download thee picture

'''
------------------------------------------------------------------------
urlretrieve() 方法直接将远程数据下载到本地。

urlretrieve(url, filename=None, reporthook=None, data=None)

参数 finename 指定了保存本地路径（如果参数未指定，urllib会生成一个临时文件保存数据。）

参数 reporthook 是一个回调函数，当连接上服务器、以及相应的数据块传输完毕时会触发该回调，我们可以利用这个回调函数来显示当前的下载进度。

参数 data 指 post 到服务器的数据，该方法返回一个包含两个元素的(filename, headers)元组，filename 表示保存到本地的路径，header 表示服务器的响应头。
------------------------------------------------------------------------
'''




from urllib import request
import re,time,os

#模拟浏览器打开页面
def getUrl(url):
	Surl = url;

	#模拟Firefox
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
	headers = {'User-Agent':user_agent}

	req = request.Request(Surl,headers = headers)
	with request.urlopen(req) as Sreq:
		Spage = Sreq.read()
		UnicodePage = Spage.decode('utf-8')
	return UnicodePage

#获取图片页面地址
def getPic(url):
	reg = r'class="il_img"><a href="(.+?)" title'
	pages = getUrl(url)
	#re.findall 把符合正则的内容以列表的方式保存
	pic = re.findall(reg,pages,re.S)
	return pic

#获取图片下载地址
def getImg(url):
	reg = r'<img id="imgis" src=\'(.+?\.jpg)\' alt=".+?" />'
	imgs = getUrl(url)
	img = re.findall(reg,imgs,re.S)
	return img[0]



#-----------------------------------------------------------------------
print ('''
------------------------------------------------------------------------
爬虫测试：爬取图片
测试网站：http://www.ivsky.com/bizhi/index_1.html
------------------------------------------------------------------------
''')
print ('正在下载图片，请稍等............................................')


#---爬取页面的地址，以第一页为例
url = 'http://www.ivsky.com/bizhi/index_1.html'

#获取图片页面地址
item = getPic(url)


#获取当前页面中的图片页面地址
for i in range(len(item)):
	pic_side_list = 'http://www.ivsky.com'+item[i]
	
	#获取从上面获得的页面内的地址
	piclist = getPic(pic_side_list)
	
    #获取下载图片的地址
	itemsList = []
	for x in range(len(piclist)):
		imgs ='http://www.ivsky.com'+piclist[x]

		#获取图片下载地址
		imgitem = getImg(imgs)
		
		print (imgitem)
		#~ exit()
		try:
			f = 'F:\\spiderpic\\'
			#创建文件夹
			os.mkdir(f)
			#以时间命名图片
			fname = time.strftime('%Y%m%d%H%M%S')
			#下载图片
			request.urlretrieve(imgitem,'%s%s.jpg' % (f,fname))
			#每下载一个，停留一秒
			time.sleep(1)
		except:
			print ('   o(︶︿︶)o  \nError!!!!!!!\n请从新运行爬虫')
			exit()

print ('  o(≧v≦)o~~ \n下载完成!!!!!!!!!!!')
print ('''
------------------------------------------------------------------------
-----------------------     爬虫结束      -------------------------------
------------------------------------------------------------------------

					   _,\,\,\|\|\|\|\|\|\|\/-\___.._
				  __,-'                           () .\
				 /  __/---\___                __   ---/
				|  /          \ \___________/\\  \___/
				| |            \ \            \\
				| |            / |             \\__/_
				| |            | \/_              /\
				 ||             \--\
				 ||                   
				  \\_______        
				   \-------\\____

------------------------------------------------------------------------				   
------------------------------------------------------------------------
''')
