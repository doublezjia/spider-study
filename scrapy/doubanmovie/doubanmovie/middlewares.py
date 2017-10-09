# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy,random,sys
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class DoubanmovieSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



# 随机请求头
class UserAgentListMiddleware(UserAgentMiddleware):
    """set User-Agent"""
    def __init__(self, user_agent):
        self.user_agent = user_agent
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            user_agent = crawler.settings.get('USER_AGENT_LIST')
            )
    def process_request(self,request,spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent

# 代理IP
class ProxyMiddleware(object):
    def process_request(self,request,spider):
        ippool = []
        ipfile = r'C:\Users\yw0682\Desktop\scrapy\scrapyspider\scrapyspider\iplist.txt'
        with open(ipfile,'r') as f:
            while f.readline():
                ippool.append(f.readline().strip())
        ip = random.choice(ippool)
        request.meta['proxy'] = ip