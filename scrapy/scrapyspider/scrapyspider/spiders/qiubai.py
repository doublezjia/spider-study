# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyspider.items import ScrapyspiderItem

class QiubaiSpider(CrawlSpider):
    name = 'qiubai'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.qiushibaike.com/users/[0-9]+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapyspiderItem()
        item['name'] = response.xpath('/html/body/div[2]/div[1]/a/img/@alt').extract_first().strip()
        item['image_urls'] = response.xpath('/html/body/div[2]/div[1]/a/img/@src').extract_first().strip()
        item['follower'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[1]/text()').extract_first().strip()
        item['follow'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[2]/text()').extract_first().strip()
        item['discuss'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[4]/text()').extract_first().strip()
        item['accelerated_again'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[3]/text()').extract_first().strip()
        item['choice'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[6]/text()').extract_first().strip()
        item['smiling_face'] = response.xpath('/html/body/div[2]/div[3]/div[1]/ul/li[5]/text()').extract_first().strip()
        yield item

