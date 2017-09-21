# Scrapy 学习笔记

[Scrapy文档](http://scrapy-chs.readthedocs.io/zh_CN/0.24/index.html)

## 安装

可以通过pip进行安装
pip install Scrapy

>注意windows要先下载安装Twisted,然后再安装Scrapy，否则Scrapy安装会出现如下错误：
>error: Unable to find vcvarsall.bat
>[Twisted下载](http://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted)
>请根据python版本进行下载
>要是运行Scrapy的时候出现win32api的错误的，可以安装这个
>[pywin32下载](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/)


## Scrapy使用

创建项目
```
scrapy startproject 项目名
```
  项目目录如下
![目录](http://ovv4v0gcw.bkt.clouddn.com/scrapy01.png)

items.py是用来定义爬取字段的
pipelines.py 是存储爬取的数据


### 编写爬虫

可以通过 `scrapy genspider 爬虫名 网址`进行新建。

参考：[Scrapy命令行](http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/commands.html#genspider)

创建一个Spider，您必须继承 `scrapy.Spider` 类， 且定义以下三个属性:

- `name`: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。

- `start_urls`: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。

- `parse()` 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。

```python
class doubanSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        "https://movie.douban.com/chart"
    ]
    def parse(self, response):
    	soup = BeautifulSoup(response.text,'html.parser')
    	data = soup.find('div',class_='indent').find_all('table')
    	for i in data:
    		# 把获取的内容放到item中
    		item['title'] = i.find('a',class_='nbg')['title']
    		item['score'] = i.find('span',class_='rating_nums').string
    		yield item
```

>如果没有特殊作用，`parse()`不要随便改名

### 运行
```
scrapy crawl name
```
Scrapy为Spider的`start_urls`属性中的每个URL创建了`scrapy.Request`对象，并将`parse`方法作为回调函数(callback)赋值给了Request。

Request对象经过调度，执行生成`scrapy.http.Response`对象并送回给spider `parse()`方法。

>这里的`name`是上面的爬虫里定义的name的名称，如上面的代码的`name`就是`test`

### 提取Item

提取网页中的数据的方法有很多，Scrapy使用了一种基于`XPath`和`CSS`表达式机制，也可以用BeautifulSoup来提取。

XPath表达式的例子及对应的含义:

- `/html/head/title`: 选择HTML文档中`<head>`标签内的`<title>`元素
- `/html/head/title/text()`: 选择上面提到的`<title>`元素的文字
- `//td`: 选择所有的`<td>`元素
- `//div[@class="mine"]`: 选择所有具有`class="mine"`属性的`div`元素


xpath提取出来的是以列表的形式保存。

提取标签的文本只要在表达式后面加上`/text()`

提取属性就加上`/@属性名`

显示提取的某个内容`response.xpath(XPath表达式).extract()[num]`
`response.xpath(XPath表达式).extract_first()`提取第一个

>PS:只要可以提取到内容，用哪个方法都可以。

参考：
- [XPath教程](http://www.w3school.com.cn/xpath/index.asp)
- [Scrapy文档 选择器](http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/selectors.html)

### 保存数据
```
scrapy crawl test -o test.json
```

### 运行时候的一些问题
1. 在调试时候可以在settings.py中取消下面几行的注释
![settings](http://ovv4v0gcw.bkt.clouddn.com/scrapy_setting01.png)
这几行注释的作用是，Scrapy会缓存你有的Requests!当你再次请求时，如果存在缓存文档则返回缓存文档，而不是去网站请求，这样既加快了本地调试速度，也减轻了 网站的压力。

2. 如果运行的时候response没有获取到内容，可能跟robot.txt有关，可以尝试关闭settings.py中的ROBOTSTXT_OBEY
![ROBOTSTXT_OBEY](http://ovv4v0gcw.bkt.clouddn.com/scrapy_setting02.png)

3. 这里设置请求头
![user_agent](http://ovv4v0gcw.bkt.clouddn.com/scrapy_setting03.png)

4. 保存成csv中文乱码的原因是因为csv的编码问题
解决方法是用notepad++等编辑工具打开然后再保存为编码格式为UTF-8 BOM 就可以了


---

## Spiders参数

内容太多，请看文档[Spiders参数](http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/spiders.html)


### start_requests
默认是使用`start_urls`的url生成Request。可以通过重写`start_requests` 可以把一些有规律的网址生成Request.

例子：
```
bash_url = 'http://www.wmpic.me/tupian/wmpic/page/'
#通过start_requests生成1到172的url
def start_requests(self):
	for i in range(1,3):
		url = self.bash_url+str(i)
		yield Request(url,self.parse)
```
---

## 通过Scrapy下载图片

定义item，在item.py中添加
```
class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	name = scrapy.Field()
	image_urls = scrapy.Field()
	image_paths = scrapy.Field()
```

下载图片要用到`ImagesPipeline`库，可以在`pipelines.py`中新建一个类，继承`ImagesPipeline`。通过重写`get_media_requests`和`item_completed`实现下载,通过重写`file_path`实现文件存放路径重写。


`pipelines.py`代码如下：
```
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

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
```
>这里要注意，`item['image_urls']`存放的是下载地址的列表，所以在写爬虫脚本的时候要把获取到的图片地址先存放在一个列表中，然后再把列表赋值到`item['image_urls']`，这样才可以。
> `file_path`中的`request.meta['item']`要在函数`get_media_requests`中Request的时候把item赋值到meta中。如`scrapy.Request(img_url,meta={'item':item,})`

在settings.py中找到`ITEM_PIPELINES`把注释去掉，把类名改为`DownloadimagePipeline`，添加文件路径`IMAGES_STORE`和文件过期时间`IMAGES_EXPIRES`。
![settings的设置](http://ovv4v0gcw.bkt.clouddn.com/scrapydownpic01.png)

参考：[Scrapy文档 下载图片](http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/images.html)

---

### 随机请求头

在settings.py中添加`USER_AGENT_LIST`的列表
![USER_AGENT_LIST](http://ovv4v0gcw.bkt.clouddn.com/scrapy_useragent01.png)

把`DOWNLOADER_MIDDLEWARES`的注释去掉，并按图片所示设置。
![DOWNLOADER_MIDDLEWARES](http://ovv4v0gcw.bkt.clouddn.com/scrapy_useragent02.png)

然后就在`middlewares.py`中添加如下类
```
import scrapy,random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

# 随机请求头
class UserAgentListMiddleware(UserAgentMiddleware):
    """set User-Agent"""
    def __init__(self, user_agent):
        self.user_agent = user_agent
    
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            user_agent = crawler.settings.get('USER_AGENT_LIST')
            )
        def process_request(self,request,spider):
            agent = random.choice(self.user_agent)
            request.headers['User-Agent'] = agent
```
---

## 代理IP设置
在`setting.py`中`DOWNLOADER_MIDDLEWARES`添加以下两句。
```
DOWNLOADER_MIDDLEWARES = {  
'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':110,
   'scrapyspider.middlewares.ProxyMiddleware':100,
}
```
在`middlewares.py`中添加如下类，
```
# 代理IP
class ProxyMiddleware(object):
    def process_request(self,request,spider):
        ippool = [
        'http://221.202.248.27:8118',
        'http://182.46.69.156:4382',
        'http://123.96.0.236:808',
        'http://113.200.36.181:80',
        'http://222.76.174.106:8118',
        'http://61.135.217.7:80',
        'http://119.55.136.97:80',
        ]
        # 随机获取代理IP，random.choice是获取列表、字典、元祖的随机值。
        ip = random.choice(ippool)
        request.meta['proxy'] = ip
```
>注意：如果代理IP无效请修改，可到这个网站上面找找免费的代理ip [点击跳转](http://www.xicidaili.com/)

参考：[Scrapy: 如何设置代理 - 简书](http://www.jianshu.com/p/b456f94cfdd3)

