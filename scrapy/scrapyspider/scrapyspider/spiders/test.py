# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['doublezjia.com']
    start_urls = ['http://doublezjia.com/']

    def parse(self, response):
        print (response.url)
