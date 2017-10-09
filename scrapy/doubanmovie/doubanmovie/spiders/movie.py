# -*- coding: utf-8 -*-
import scrapy,sys,io
from bs4 import BeautifulSoup
from doubanmovie.items import DoubanmovieItem
from scrapy.http import Request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    bash_url = 'https://movie.douban.com/top250?start='
    # def start_requests(self):
    # 	for i in range(0,250,25):
    # 		url = self.bash_url+str(i)
    # 		yield Request(url,self.parse)
    def parse(self, response):
        soup = BeautifulSoup(response.text,'html.parser')
        data = soup.find('ol',class_='grid_view').find_all('li')
        item = DoubanmovieItem()
        for i in data:
            title = i.find('div',class_='hd').find('span',class_='title').string
            msg = i.find('div',class_='bd').find('p').text
            msglist = msg.strip().split('\n')
            cast = msglist[0]
            reldate = msglist[1]
            ratingnum = i.find('div',class_='star').find('span',class_='rating_num').string
            quote = i.find('p',class_='quote').find('span',class_='inq').string
            item['title'] = title.strip()
            item['cast'] = cast.strip()
            item['reldate'] = reldate.strip()
            item['ratingnum'] = ratingnum.strip()
            item['quote'] = quote.strip()
            yield item
            # print (title.strip())
            # print (cast.strip())
            # print (reldate.strip())
            # print (ratingnum.strip())
            # print (quote.strip())
