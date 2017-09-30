# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy,pymysql,datetime
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        return item

# 下载图片
class DownloadimagePipeline(ImagesPipeline):
	def get_media_requests(self,item,info):
		for img_url in item['image_urls']:
			try:
				yield scrapy.Request(img_url,meta={'item':item,})
			except:
				pass
			
	def item_completed(self,results,item,info):
		image_paths = [x['path'] for ok,x in results if ok]
		if not image_paths:
			raise DropItem('Item contains no images')
		item['image_paths'] = image_paths
		return item
	# 重写文件名，这里的request.meta要从get_media_requests传过来，最后返回文件名
	def file_path(self,request,response=None,info=None):
		item = request.meta['item']
		folder = item['name']
		image_guid = request.url.split('/')[-1]
		filename = r'full/{0}/{1}'.format(folder,image_guid)
		return filename

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
		curTime = datetime.datetime.now()
		# 执行插入语句
		self.cursor.execute('select name from qiubai where name = %s',(item['name'].encode('utf-8')))
		
		# fetchall() 返回多个元组，即返回多个记录(rows),如果没有结果 则返回 ()
		sel = self.cursor.fetchall()
		# print (sel)
		if len(sel) == 0 :
			self.cursor.execute(
				'insert into qiubai(name,follower,follow,discuss,accelerated_again,choice,smiling_face,avatar,curtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
				(item['name'].encode('utf-8'),item['follower'].encode('utf-8'),
					item['follow'].encode('utf-8'),item['discuss'].encode('utf-8'),
					item['accelerated_again'].encode('utf-8'),item['choice'].encode('utf-8'),
					item['smiling_face'].encode('utf-8'),item['image_urls'].encode('utf-8'),curTime)
				)
			self.conn.commit()
		return item

		