#!/usr/bin/env python3
#_*_ coding: utf-8 _*_

from urllib import request
import re,sys,io,requests,re,os,time,threading,threadpool,asyncio



'''
------------------------------------------------------------------------------------
乱码问题

在python3里，有几点关于编码的常识

1.字符就是unicode字符，字符串就是unicode字符数组
2.str转bytes叫encode，bytes转str叫decode，如上面的代码就是将抓到的字节流给decode成unicode数组

编码不对就会出现类似错误，特别是Windows下：
UnicodeEncodeError: 'gbk' codec can't encode character '\xbb' in position 0: illegal multibyte sequence


系统是win7的，python的默认编码不是'utf-8',改一下python的默认编码成'utf-8'
就要用到下面的代码：

要引用sys和io模块
-------------------------------------------------------------------------------------
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
--------------------------------------------------------------------------------------
编码名称 	用途
utf8 		所有语言
gbk 		简体中文
gb2312 		简体中文
gb18030 	简体中文
big5 		繁体中文
big5hkscs 	繁体中文
--------------------------------------------------------------------------------------
如果UTF8会出现乱码，可以试一下其他编码
--------------------------------------------------------------------------------------

requests 是Python的第三方库，要安装，可以通过 pip install requests 来安装，使用跟urllib类似
Requests 是用Python语言编写，基于 urllib，采用 Apache2 Licensed 开源协议的 HTTP 库。它比 urllib 更加方便，可以节约我们大量的工作，完全满足 HTTP 测试需求。
Requests 的哲学是以 PEP 20 的习语为中心开发的，所以它比 urllib 更加 Pythoner。更重要的一点是它支持 Python3

具体使用可以参考：http://blog.csdn.net/shanzhizi/article/details/50903748
---------------------------------------------------------------------------------------
'''





#改变标准输出的默认编码
#~ sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

#打开页面
def getpage(url):
	url = url
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
	data = {'some': 'data'}
	headers = {'User-Agent':user_agent}
	cookies = {'is_click':'1'}

	#通过requests来连接网站，因为测试网站有个带cookies的点击事件，所以通过带上cookies来进行连接。
	req = requests.post(url,data=data,headers=headers,cookies=cookies)
	return req.text

#获取页面中所有图片页面的地址
def get_pic_page(url):
	url = url
	reg = r'<div class="title"><a href="(.*?)">.*?</a></div>'
	page = re.findall(reg,getpage(url),re.S)
	return page

#获取图片的下载地址
def get_Img_url(url):
	url = url
	reg = r'<div style=\'padding-top: 5px;\'><a href=\'(.+?\.jpg|.+?\.JPG.+?\.png|.+?\.PNG)\' download=\'\' target=\'_blank\'><i>查看原图</i>'
	images = re.findall(reg,getpage(url),re.S)
	return images[0]

#下载图片
def downloadImg(imgurl):
	imgurl = imgurl
	files = 'F:\\TOPIT.ME\\'
	fname = time.strftime('%Y%m%d%H%M%S')
	
	if os.path.isdir(files):
		pass
	else:
		os.mkdir(files)
	try:
		request.urlretrieve(imgurl,'%s%s.jpg' % (files,fname))
		#~ time.sleep(1)
	except:
		print ('Error!!!!!!')
		sys.exit()

#-----------------------------------------------------------------------------

print ('''
------------------------------------------------------------------------
爬虫测试：爬取图片
测试网站：http://www.topit.me/?p=1
------------------------------------------------------------------------
''')

url = 'http://www.topit.me/?p=1'
item = get_pic_page(url)

for i in item:
	imgurl = get_Img_url(i)
	print (imgurl)
	
	t = threading.Thread(target=downloadImg,args=(imgurl,))
	t.start()
	time.sleep(1)
	t.join()

	#~ pool = threadpool.ThreadPool(5)
	#~ requests = threadpool.makeRequests(downloadImg, (imgurl,))
	#~ [pool.putRequest(req) for req in requests]
	#~ pool.wait()




print ('''
------------------------------------------------------------------------
爬虫结束
------------------------------------------------------------------------
''')






