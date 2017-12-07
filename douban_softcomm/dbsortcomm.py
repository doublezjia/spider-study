#!/usr/bin/env python3
#-*- coding:utf8 -*- 
# 豆瓣短评评分统计
#
# 运行要先安装 requests库和BeautifulSoup库
#
# 通过pyecharts实现图表生成，要先安装pyecharts
# pyecharts文档：https://github.com/chenjiandongx/pyecharts

# 想修改词云图片可以替换wordcloud_img中的bg.jpg(名称为bg,后缀只能为jpg)
# 运行前先登陆豆瓣获取cookies生成cookies.txt文件
# 默认统计结果为寻梦环游记

# 统计结果会生成到file文件夹中
# file中生成的文件说明：
# comment.txt 	爬去的短评内容，用于生成词云
# rating.html 	统计结果的图表，以网页的形式显示
# wordcloud.png 	词云图片

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
bash_url = 'https://movie.douban.com/subject/{num}/comments{pg}'

# 定义星级统计变量
zerostar=0;firstar=0;secstar=0;thistar=0;foustar=0;fifstar=0;

# 统计评分并生成图表
def get_douban_rating(pg_url,pg_num,echart_title):
	# 全局变量
	global zerostar,firstar,secstar,thistar,foustar,fifstar
	# 页面链接数字
	pg_num = pg_num
	# 生成图表时用的标题
	echart_title=echart_title
	# 获取cookies
	cookies = dbcookies()
	print('开始爬去页面内容')
	# 通过requests获取页面
	# url 完整页面地址
	url = bash_url.format(pg=pg_url,num=pg_num)
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
			try:
				ratingdata = item.find(class_='comment').find(class_='comment-info').find(class_='rating')
			except AttributeError as e:
				print ('获取内容出错')
				print ('错误内容为：'+e)
				sys.exit('退出运行')

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

			# 把每个评论正文存放在./file/comment.txt中
			comment=item.find(class_='comment').p.text.strip()
			with open('./file/comment.txt','a',encoding='utf-8') as f:
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
				# 回传到 get_douban_rating(pageurl,pg_num,echart_title)
				return get_douban_rating(pageurl,pg_num,echart_title)
			else:
				print ('爬去结束')
		else:
			# 获取下一页地址
			pageurl = pagedata.find('a',class_='next')['href']

			print('页面爬去结束，准备爬去下一页')
			# 不要跑太快，暂停一下
			time.sleep(4)
			# 回传到 get_douban_rating(pageurl,pg_num,echart_title)
			return get_douban_rating(pageurl,pg_num,echart_title)


		# 图表生成
		# 饼图
		print ('生成图表')
		attr = ['没有评分','1星','2星','3星','4星','5星']
		pie = Pie('%s短评评星百分比' % echart_title,'数据来源豆瓣',width=900,title_pos='center')
		pie.add('',attr,rating_percent_list,is_label_show=True,radius=[0,50],legend_pos='left',legend_orient='vertical')

		# # 柱状图
		bar = Bar('%s短评评星人数' % echart_title,'数据来源豆瓣',width=900,title_pos='center')
		bar.add('',attr,ratingstart_num_list,is_stack=True)

		# 全部图表在同一个页面显示
		page = Page()
		page.add(bar)
		page.add(pie)
		page.render('./file/rating.html')
		print('图表生成结束,文件在file文件夹中,名称为：rating.html')
	else:
		print ('连接网站出错,错误状态码为：%s' % req.status_code)
		print ('错误页面：%s' % url)
		sys.exit('停止运行，自动退出！！！')

# 把cookies存放到字典中
def dbcookies():
	if not os.path.isfile('./cookies/cookies.txt'):
		print ('没有cookies.txt文件')
		sys.exit('自动退出')
	f_cookies = open('./cookies/cookies.txt', 'r')
	cookies = {}
	for line in f_cookies.read().split(';'):
		name, value = line.strip().split('=', 1)
		cookies[name] = value
	return cookies

# 词云
def douban_wordcloud(bg):
	# 判读文件是否存在
	if not os.path.isfile('./file/comment.txt'):
		print ('文件夹file中没有comment.txt这个文件可生成词云')
		sys.exit('自动退出')
	print('开始生成词云')
	file = './file/comment.txt'
	# 读取文本
	with open(file,'r',encoding='utf8') as f:
		coco_content = f.read()
	# jieba 分词，先把获取的内容分词保存到Scut，然后把分词以换行的形式保存到dcut变量中
	Scut = jieba.cut(coco_content,cut_all=False)
	dcut = '\n'.join(Scut)

	#词云停用词
	STOPWORDS= {}.fromkeys([line.rstrip() for line in open('stopwords.txt','r',encoding='utf8')])
	# 背景图片
	backgroudimage=bg
	backgroud_Image = plt.imread(backgroudimage)
	# 设置wordcloud
	wc = WordCloud( background_color = '#fff',    				# 设置背景颜色
	                mask = backgroud_Image,        				# 设置背景图片
	                max_words = 2000,            				# 设置最大现实的字数
	                stopwords = STOPWORDS,                  	# 设置停用词
	                font_path = './fonts/wqy-microhei.ttc',  	# 设置字体格式，如不设置显示不了中文
	                max_font_size = 200,                     	# 设置字体最大值
	                random_state = 30,            				# 设置有多少种随机生成状态，即有多少种配色方案
	                )
	wc.generate(dcut)
	image_colors = ImageColorGenerator(backgroud_Image)
	wc.recolor(color_func = image_colors)
	plt.imshow(wc)
	plt.axis('off')

	# 显示词云图片
	# plt.show()
	# 保存词云图片
	plt.savefig('./file/wordcloud.png')
	print ('生成词云图片成功,文件存放在file文件夹中,名称为：wordcloud.png')
	print ('运行结束')

# 主函数
def main(num='20495023',echart_title='寻梦环游记',bg='./wordcloud_img/bg.jpg'):
	# 页面链接数字
	num = num
	# 生成图表时用的标题
	echart_title=echart_title
	# 词云背景图片
	backgroudimage=bg

	# 开始页面地址
	# 最新短评
	# new_comm_page = '?start=0&limit=0&sort=time&status=P&percent_type='
	# 热门短评
	hot_comm_page = '?start=0&limit=0&sort=new_score&status=P&percent_type='

	# 第一次运行 判断文本是否存在 要是存在的就删除
	if os.path.isfile('./file/comment.txt'):
		os.remove('./file/comment.txt')

	get_douban_rating(hot_comm_page,num,echart_title)
	douban_wordcloud(backgroudimage)	


if __name__ == '__main__':
	tip = '''
++++++++++++++++++++++++++++++++++++++++++++++++++++
豆瓣电影电视剧短评评分统计

想修改词云图片可以替换wordcloud_img中的bg.jpg(名称为bg,后缀只能为jpg)
运行前先登陆豆瓣获取cookies生成cookies.txt文件
默认统计结果为寻梦环游记

统计结果会生成到file文件夹中
file中生成的文件说明：
comment.txt 	爬去的短评内容，用于生成词云
rating.html 	统计结果的图表，以网页的形式显示
wordcloud.png 	词云图片

退出请输入q

++++++++++++++++++++++++++++++++++++++++++++++++++++
	'''
	print (tip)

	title = input('片名[不填默认为寻梦环游记]：')
	if title == 'q':
		sys.exit('退出运行')

	page_num = input('页面链接数字(如:20495023)[不填默认为寻梦环游记的页面链接]：')
	if page_num == 'q':
		sys.exit('退出运行')

	# bgimg = input('词云图片(如没有的就默认)：')
	if title !='' and page_num !='':
		main(num=page_num,echart_title=title)
	else:
		main()
	