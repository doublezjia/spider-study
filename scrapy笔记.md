# Scrapy笔记
---

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