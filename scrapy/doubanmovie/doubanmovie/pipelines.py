# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy,pymysql,datetime

class DoubanmoviePipeline(object):
    def process_item(self, item, spider):
        return item


# 把数据保存到Mysql中
class MySQLStorePipeline(object):
	def __init__(self):
		# 数据库信息
		sqlconfig={
		'user': 'root',
		'password':'root',
		'db':'scrapy',
		'host': '127.0.0.1',
		'port': 3306,
		}
		# 连接数据库，**sqlconfig这个意思等于 user='root',password='root'等，表示关键字参数。
		self.conn = pymysql.connect(**sqlconfig)
		self.cursor = self.conn.cursor()

	def process_item(self,item,spider):
		addTime = datetime.datetime.now()
		# 执行插入语句
		self.cursor.execute('select title from douban_movie where title = %s',(item['title'].encode('utf-8')))
		
		# fetchall() 返回多个元组，即返回多个记录(rows),如果没有结果 则返回 ()
		sel = self.cursor.fetchall()
		# print (sel)
		if len(sel) == 0 :
			self.cursor.execute(
				'insert into douban_movie(title,cast,reldate,ratingnum,quote,addtime) values(%s,%s,%s,%s,%s,%s)',
				(item['title'].encode('utf-8'),item['cast'].encode('utf-8'),item['reldate'].encode('utf-8'),
					item['ratingnum'].encode('utf-8'),item['quote'].encode('utf-8'),addTime)
				)
			self.conn.commit()
		return item