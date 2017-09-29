# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest

class TestSpider(scrapy.Spider):
    name = 'logintest'
    # allowed_domains = ['www.wpdaxue.com']
    # start_urls = ['http://doublezjia.com/']\
    def start_requests(self):
    	return [Request('https://www.wpdaxue.com/login/',callback=self.login)]
    def login(self,response):
    	redirect=response.xpath('//*[@id="loginform"]/p[4]/input[2]/@value').extract_first()
    	wpuf_login = response.xpath('//*[@id="loginform"]/p[4]/input[3]/@value').extract_first()
    	wpnonce = response.xpath('//*[@id="_wpnonce"]/@value').extract_first()
    	action = response.xpath('//*[@id="loginform"]/p[4]/input[4]/@value').extract_first()
    	wp_http_referer = response.xpath('//*[@id="loginform"]/p[4]/input[6]/@value').extract_first()
    	return [FormRequest.from_response(
    		response,url='https://www.wpdaxue.com/login/',method='post',
    		formdata={
    		'log':'scrapy',
    		'pwd':'scrapy123',
    		'redirect_to':redirect,
    		'wpuf_login':wpuf_login,
    		'action':action,
    		'_wpnonce':wpnonce,
    		'_wp_http_referer':wp_http_referer
    		},
    		callback=self.after_login
    		)]
    def after_login(self,response):
    	return [Request('https://www.wpdaxue.com/user/my-posts/',callback=self.parse)]
    def parse(self, response):
    	count = response.xpath('//*[@id="the-post"]/div[1]/div[1]/div[2]/text()').extract_first()
    	print (count)
