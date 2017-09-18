# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        return item

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