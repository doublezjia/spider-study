# -*- coding: utf-8 -*-
import scrapy
from scrapyspider.items import ScrapyspiderItem

class QbSpider(scrapy.Spider):
    name = 'qb'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/users/31216386/']

    def parse(self, response):
        item = ScrapyspiderItem()
        item['user'] = response.xpath('/html/body/div[2]/div[1]/a/img/@alt').extract_first().strip()
        item['follower'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[1]/text()').extract_first().strip()
        item['follow'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[2]/text()').extract_first().strip()
        item['discuss'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[4]/text()').extract_first().strip()
        item['accelerated_again'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[3]/text()').extract_first().strip()
        item['choice'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[6]/text()').extract_first().strip()
        item['smiling_face'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[5]/text()').extract_first().strip()
        yield item
