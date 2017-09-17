# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from pyspider.items import PyspiderItem
from scrapy.http import Request

class WmpicSpider(scrapy.Spider):
	name = 'wmpic'
	allowed_domains = ['www.wmpic.me']
	# start_urls = ['http://www.wmpic.me/tupian/wmpic/']
	bash_url = 'http://www.wmpic.me/tupian/wmpic/page/'
	imgurl = []

	#通过start_requests生成1到172的url
	def start_requests(self):
		for i in range(1,3):
			url = self.bash_url+str(i)
			yield Request(url,self.parse)
	def parse(self, response):
		item = PyspiderItem()
		soup = BeautifulSoup(response.body,'html.parser')
		data = soup.find('ul',class_='item_list').find_all('div',class_='post')
		for i in data:
			self.imgurl.append(i.find('img')['src'])
		# 因为传递到pipeline中的是列表，所以这里把获取的地址添加到imgurl列表中
		# 然后把列表赋值到item['image_urls']这个字段中。
		item['image_urls'] = self.imgurl
		# 获取名称并且去掉空格，因为xpath获取的是列表
		item['name'] = response.xpath('//*[@id="mainbox"]/ul/li[1]/div[2]/h2/a/text()').extract()[0].strip()
		# print (item['name'])
		yield item
