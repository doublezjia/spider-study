#coding: utf-8
#

import os,sys,datetime,requests,io,pygal
from bs4 import BeautifulSoup

# 出现乱码的时候可以用这个,encoding可以输utf8,gbk,gb2312,gb18030,big5,big5hkscs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

page_url = 'https://book.douban.com/top250?icn=index-book250-all'
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}


def page_url_list():
	score = []
	req = requests.get(page_url,headers=headers)
	soup = BeautifulSoup(req.text,'html.parser')
	data = soup.find('div',class_='indent').find_all('table')
	for item in data:
		name = item.find('div',class_='star clearfix').find('span',class_='rating_nums')
		score.append(name.string)
	return score


def content_score():
	req = requests.get(page_url,headers=headers)
	soup = BeautifulSoup(req.text,'html.parser')	
	data = soup.find('div',class_='rating_self clearfix')
	print (data)


def draw_histogram():
	score = page_url_list()
	hist = pygal.Bar()
	hist.title = '豆瓣'
	hist.x_lables = map(str,range(10))
	hist.x_title = '分数'
	hist.y_title = '数量'
	hist.add('count',score)
	hist.render_to_file('douban_score.svg')

if __name__ == '__main__':
	page_url_list()