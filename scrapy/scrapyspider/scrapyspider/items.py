# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
	name = scrapy.Field()
	image_urls = scrapy.Field()
	image_paths = scrapy.Field()
	
	# temperature = scrapy.Field()

	# # 用户名
	# user = scrapy.Field()
	# # 粉丝
	# follower = scrapy.Field()
	# # 关注
	# follow = scrapy.Field()
	# # 评论
	# discuss = scrapy.Field()
	# # 糗事
	# accelerated_again = scrapy.Field()
	# #精选
	# choice = scrapy.Field()
	# # 笑脸
	# smiling_face = scrapy.Field()