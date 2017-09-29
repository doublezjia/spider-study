# -*- coding: utf-8 -*-
import scrapy
from scrapyspider.items import ScrapyspiderItem
from bs4 import BeautifulSoup

class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['www.weather.com.cn']
    start_urls = ['http://www.weather.com.cn/weather1d/101280101.shtml']

    def parse(self, response):
        name = response.xpath('//*[@id="around"]/div[1]/ul/li/a/span/text()').extract()
        temp = response.xpath('//*[@id="around"]/div[1]/ul/li/a/i/text()').extract()
        item = ScrapyspiderItem()
        for i in range(len(name)):
        	item['name'] = name[i]
        	item['temperature'] = temp[i]
        	yield item
