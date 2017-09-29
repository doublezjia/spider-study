# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy,random,sys
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapyspider.proxysip import Porxysip

class ScrapyspiderSpiderMiddleware(object):
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

        # 以下三个方法只能运行一个，用一个请把另外的注释掉
        # 随机获取代理IP，random.choice是获取列表、字典、元祖的随机值。

        # 第一种
        # 在ippool中手工添加代理ip
        # ippool = [
        # 'http://221.202.248.27:8118',
        # 'http://182.46.69.156:4382',
        # 'http://183.47.136.193:8118',
        # 'http://113.200.36.181:80',
        # 'http://222.76.174.106:8118',
        # 'http://61.135.217.7:80',
        # 'http://111.224.147.16:8118',
        # ]
        # ip = random.choice(ippool)

        # 第二种
        # 先通过proxysip.py生成TXT文本，然后在这里读取文本的代理IP 
        # 代理ip列表文件路径,要修改。如果没有这个文件的请运行一下proxysip.py
        ippool = []
        ipfile = r'C:\Users\yw0682\Desktop\scrapy\scrapyspider\scrapyspider\iplist.txt'
        with open(ipfile,'r') as f:
            while f.readline():
                ippool.append(f.readline().strip())
        ip = random.choice(ippool)

        # 第三种
        # 不读取文本,直接通过Porxysip()获取代理IP
        # ippool = Porxysip()
        # ip = random.choice(ippool.getaddress())
        
        # 这个不用注释,使用代理IP
        request.meta['proxy'] = ip