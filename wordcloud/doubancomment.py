import os,requests,sys,io,re,csv,codecs,json,jieba,time,datetime
from bs4 import BeautifulSoup
from lxml import etree
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import matplotlib.pyplot as plt

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

base_url = 'https://movie.douban.com/subject/26322642/reviews?start={num}'
rurl='https://movie.douban.com/j/review/{num}/full'

# 获取评论
def get_content(filename='douban'):
	pagenum = 1
	file=filename+'.txt'
	if os.path.isfile(file):
		os.remove(file)
	for page in range(0,200,20):
		url = base_url.format(num=str(page))
		print ('正在获取第%s页评论....' % pagenum)
		# 获取评论页面
		req = requests.get(url,headers=headers)
		if req.status_code == 200:
			soup=BeautifulSoup(req.text,'html.parser')
			data = soup.find(class_='review-list').find_all(attrs={'typeof':'v:Review'})
			for item in data:
				Rurl = rurl.format(num=item['data-cid'])
				# 获取评论
				Req=requests.get(Rurl,headers=headers)
				# 获取json中的内容
				html = Req.json()['html'].strip()

				# 去除html标签
				rehtml = re.compile(r'<[^>]+>|&nbsp;',re.S)
				content = rehtml.sub('',html)

				# 写入文本
				with codecs.open(file,'a','utf8') as f:
					f.write(content+'\n\n')
		print('第%s页获取成功...' % pagenum)
		pagenum=pagenum+1
		for t in range(1,11):
			print ('等待%s秒' % t)
			time.sleep(1)
	print ('获取评论完毕....')
	return file

#生成词云
def content_wordcloub(file='db.txt',bg='bg.jpg'):
	print ('正在生成词云图片....')
	backgroudimage=bg
	if os.path.isfile(file):
		# 读取文本
		with codecs.open(file,'rb','utf8') as f:
			lstxt=f.read()
		# jieba 分词
		Scut= jieba.cut(lstxt)
		dcut='\n'.join(Scut)

		#词云停用词
		STOPWORDS= {}.fromkeys([line.rstrip() for line in codecs.open('stopwords.txt','rb','utf8')])
		
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


if __name__=='__main__':
	file = get_content()
	content_wordcloub(file)