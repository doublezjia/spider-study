#coding:utf-8
from scrapystudy.items import ScrapystudyItem
import scrapy,sys,io,pygal
from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

class HuxiuSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        "https://movie.douban.com/chart"
    ]
    def parse(self, response):
    	soup = BeautifulSoup(response.text,'html.parser')
    	data = soup.find('div',class_='indent').find_all('table')
    	item = ScrapystudyItem()
    	line = pygal.Bar()
    	line.title = '豆瓣电影评分'
    	line.y_title = '评分'
    	for i in data:
    		# 把获取的内容放到item中
    		# item['title'] = i.find('a',class_='nbg')['title']
    		# item['score'] = i.find('span',class_='rating_nums').string
    		# yield item
    		
    		# 通过pygal把获取的内容生成表格
    		mov_name = i.find('a',class_='nbg')['title']
    		mov_score = i.find('span',class_='rating_nums').string
    		line.add(mov_name,float(mov_score))
    	line.render_to_file('douban_score.svg')