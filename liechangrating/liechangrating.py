#!/usr/bin/env python3
#-*- coding:utf8 -*- 
# 猎场短评评分统计
#
# 运行要先安装 requests库和BeautifulSoup库
#
# 通过pyecharts实现图表生成，要先安装pyecharts
# pyecharts文档：https://github.com/chenjiandongx/pyecharts
# 
# 
# 目标页面：https://movie.douban.com/subject/26322642/comments?
#
# 使用前要先新建豆瓣cookies.txt登录文件,可通过chrome的开发者工具中的Network中复制cookie
# 然后保存为cookies.txt
#

import os,requests,sys,time,random,jieba
from pyecharts import *
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# 请求头
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

# 基本页面地址
bash_url = 'https://movie.douban.com/subject/26322642/comments{pg}'

# 开始页面地址
# 最新短评
# beginpage = '?start=0&limit=0&sort=time&status=P&percent_type='
# 热门短评
beginpage = '?start=0&limit=0&sort=new_score&status=P&percent_type='

# 定义星级统计变量
zerostar=0;firstar=0;secstar=0;thistar=0;foustar=0;fifstar=0;

def get_lc_rating(pgurl):
	# 全局变量
	global zerostar,firstar,secstar,thistar,foustar,fifstar
	cookies = dbcookies()
	# print (cookies)
	print('开始爬去页面内容')
	# 通过requests获取页面
	# url 完整页面地址
	url = bash_url.format(pg=pgurl)
	req = requests.get(url,headers=headers,cookies=cookies)
	req.encoding='utf-8'

	# 判断是否连接正常
	if req.status_code == 200 :
		soup = BeautifulSoup(req.text,'html.parser')

		# 获取内容
		commentdata=soup.find(id='comments').find_all(class_='comment-item')
		for item in commentdata:
			# 呢称
			# name = item.find(class_='comment').find(class_='comment-info').a.text.strip()

			# 评星
			ratingdata = item.find(class_='comment').find(class_='comment-info').find(class_='rating')

			# 如果有评分的 事件为True，即ratingdata能获取到内容的
			if ratingdata:
				ratingtitle = ratingdata['title']

				# 判断评级,rating变量可以注释掉,不会有影响,原来是想输出用的,现在不用
				if ratingtitle == '很差':
					# rating = 1
					firstar = firstar+1
				elif ratingtitle == '较差':
					# rating = 2
					secstar = secstar+1
				elif ratingtitle == '还行':
					# rating = 3
					thistar = thistar+1
				elif ratingtitle == '推荐':
					# rating = 4
					foustar = foustar+1
				elif ratingtitle == '力荐':
					# rating = 5
					fifstar = fifstar+1
			else:
				# rating = 0
				zerostar = zerostar+1

			# 把每个评论正文存放在lc.txt中
			comment=item.find(class_='comment').p.text.strip()
			with open('lc.txt','a',encoding='utf-8') as f:
				f.write(comment+'\n')

		# 评星总数
		ratingsum = zerostar+firstar+secstar+thistar+foustar+fifstar

		# 各个星级数量列表
		ratingstart_num_list = [zerostar,firstar,secstar,thistar,foustar,fifstar]

		# 各个星级占评星总数的百分比
		rating_percent_list = [
								round((zerostar/ratingsum)*100,2),
								round((firstar/ratingsum)*100,2),
								round((secstar/ratingsum)*100,2),
								round((thistar/ratingsum)*100,2),
								round((foustar/ratingsum)*100,2),
								round((fifstar/ratingsum)*100,2)
							]

		# 分页,把获取的页面地址回调到函数, 如果到最后了就结束.
		pagedata = soup.find(id='paginator')

		# 判断是否获取到内容，是为True
		if pagedata.span:
			pagenum= pagedata.span.text

			# 判断是否为最后一页
			if pagenum != '后页 >':
				# 获取下一页地址
				pageurl = pagedata.a['href']

				print('页面爬去结束，准备爬去下一页')
				# 不要跑太快，暂停一下
				time.sleep(4)
				# 回传到 get_lc_rating(pageurl)
				return get_lc_rating(pageurl)
			else:
				print ('爬去结束')
		else:
			# 获取下一页地址
			pageurl = pagedata.find('a',class_='next')['href']

			print('页面爬去结束，准备爬去下一页')
			# 不要跑太快，暂停一下
			time.sleep(4)
			# 回传到 get_lc_rating(pageurl)
			return get_lc_rating(pageurl)


		# 图表生成
		# 饼图
		print ('生成图表')
		attr = ['没有评分','1星','2星','3星','4星','5星']
		pie = Pie('豆瓣猎场短评评星百分比',width=900,title_pos='center')
		pie.add('',attr,rating_percent_list,is_label_show=True,legend_pos='left',legend_orient='vertical')
		# pie.render('lcpie.html')

		# # 柱状图
		bar = Bar('豆瓣猎场短评评星人数',width=900,title_pos='center')
		bar.add('',attr,ratingstart_num_list,is_stack=True)
		# bar.render('lcbar.html')

		# 全部图表在同一个页面显示
		page = Page()
		page.add(bar)
		page.add(pie)
		page.render('liechang.html')
		print('图表生成结束,名称为：liechang.html')
	else:
		print ('连接网站出错,错误状态码为：%s' % req.status_code)
		print ('错误页面：%s' % url)

def dbcookies():
	if not os.path.isfile('cookie.txt'):
		print ('没有cookie.txt文件')
		sys.exit('自动退出')
	f_cookies = open('cookie.txt', 'r')
	cookies = {}
	for line in f_cookies.read().split(';'):
		name, value = line.strip().split('=', 1)
		cookies[name] = value
	return cookies

def lc_wordcloud():
	# 判读文件是否存在
	if not os.path.isfile('lc.txt'):
		print ('没有lc.txt这个文件可生成词云')
		sys.exit('自动退出')
	print('开始生成词云')
	file = 'lc.txt'
	# 读取文本
	with open(file,'r',encoding='utf8') as f:
		lc_content = f.read()
	# jieba 分词
	Scut = jieba.cut(lc_content,cut_all=False)
	dcut = '\n'.join(Scut)

	#词云停用词
	STOPWORDS= {}.fromkeys([line.rstrip() for line in open('stopwords.txt','r',encoding='utf8')])
	backgroudimage='bg.jpg'
	backgroud_Image = plt.imread(backgroudimage)
	# 设置wordcloud
	wc = WordCloud( background_color = '#fff',    # 设置背景颜色
	                mask = backgroud_Image,        # 设置背景图片
	                max_words = 2000,            # 设置最大现实的字数
	                stopwords = STOPWORDS,        # 设置停用词
	                font_path = './msyh.ttf',# 设置字体格式，如不设置显示不了中文
	                max_font_size = 200,            # 设置字体最大值
	                random_state = 30,            # 设置有多少种随机生成状态，即有多少种配色方案
	                )
	wc.generate(dcut)
	image_colors = ImageColorGenerator(backgroud_Image)
	wc.recolor(color_func = image_colors)
	plt.imshow(wc)
	plt.axis('off')
	plt.show()

if __name__ == '__main__':
	# 第一次运行 判断文本是否存在 要是存在的就删除
	if os.path.isfile('lc.txt'):
		os.remove('lc.txt')
	get_lc_rating(beginpage)
	lc_wordcloud()
	