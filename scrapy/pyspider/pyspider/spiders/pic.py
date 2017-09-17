# -*- coding: utf-8 -*-
import scrapy,sys
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from pyspider.items import PyspiderItem

class PicSpider(CrawlSpider):
    name = 'pic'
    allowed_domains = ['www.wmpic.me']
    start_urls = ['http://www.wmpic.me/']

    # 设置规则只匹配类似这样的http://www.wmpic.me/90488地址
    rules = (
        Rule(LinkExtractor(allow='http://www.wmpic.me/[0-9]*$',deny='http://www.wmpic.me/[0-9]+/[a-zA-Z0-9_]+'), callback='parse_item', follow=True),
    )
    # 把获取的图片链接存在这个数组
    imageurl = []
    def parse_item(self, response):
        # print(response.url)
        item = PyspiderItem()
        soup = BeautifulSoup(response.body,'html.parser')
        try:
            data = soup.find('div',class_='content-c').find_all('img')
            for i in data:
                self.imageurl.append(i['src'])
                title = i['alt']
            item['name'] = title
            item['image_urls'] = self.imageurl
            yield item
        except:
            pass


