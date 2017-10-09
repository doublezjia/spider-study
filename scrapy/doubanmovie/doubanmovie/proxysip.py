#代理ip
#获取代理IP地址：www.66ip.cn

import sys,requests,io,socket,os
from bs4 import BeautifulSoup
from urllib import request
from lxml import etree

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

class Porxysip(object):
	def __init__(self):
		self.headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
		}
		self.bash_url = r'http://www.66ip.cn/'
	def getaddress(self):
		iplist = []
		for page in range(1,3):
			if page == 1:
				url = self.bash_url+'index.html'
			else:
				url = self.bash_url+str(page)+'.html'
			req = requests.get(url,headers=self.headers)
			soup = BeautifulSoup(req.text,'lxml')
			data = soup.find('div',class_='containerbox boxindex').find('table').find_all('tr')
		
			for item in data:
				add = item.find_all('td')[0].string
				addport = item.find_all('td')[1].string	
				if add != 'ip' :
					ipadd = 'http://'+add+':'+addport
					iplist.append(ipadd)
		return iplist

if __name__ == '__main__':
	ippool = Porxysip()
	# 如果有这个文件的就先删除文件
	if os.path.isfile('iplist.txt'):
		os.remove('iplist.txt')
	# 把获取的内容写入文件
	for i in ippool.getaddress():
		with open('iplist.txt','a') as f:
			f.write(i+'\n')
