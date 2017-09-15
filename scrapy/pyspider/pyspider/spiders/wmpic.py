# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from pyspider.items import PyspiderItem

class WmpicSpider(scrapy.Spider):
	name = 'wmpic'
	allowed_domains = ['www.wmpic.me']
	start_urls = ['http://www.wmpic.me/tupian/wmpic']
	imgurl = []
	def parse(self, response):
		item = PyspiderItem()
		soup = BeautifulSoup(response.body,'html.parser')
		data = soup.find('ul',class_='item_list').find_all('div',class_='post')
		for i in data:
			self.imgurl.append(i.find('img')['src'])
		item['image_urls'] = self.imgurl
		yield item
