> 爬虫环境：Python3.5

### 本爬虫是用来下载我的英雄学院的漫画

爬的地址为:[http://manhua.fzdm.com/131/](http://manhua.fzdm.com/131/)

需要安装`BeautifulSoup`库和`selenium`库，可以通过`pip`安装

```
pip install beautifulsoup4

pip install selenium
```

爬虫通过`selenium`+`PhantomJS`读取页面中JavaScript生成的图片地址

爬虫可以判断系统为`Windows`还是`Linux`,然后执行相应的`PhantomJS`

通过`platform.system`获取系统信息，判断系统

`PhantomJS`是个无界面的浏览器。


爬去的漫画存放在以漫画名命名的文件夹中，每一话以话数为文件夹，每一页以页数为文件名

默认是从第一话开始,所以默认ep='01',如果默认为第一卷的请在main中添加参数 ep='Vol_001'

如果爬去其他漫画的请修改bash_url中的地址，如地址中的131代表的是我的英雄学院，其他的请修改相应的数字，具体请观察网站本身。

如果要爬新的漫画请先把spider-urllist.log文件删除了，然后再运行爬虫。



### 文件说明：

`comic.py` 爬虫脚本

`spider-urllist.log` 存放爬去的页面地址，以便下次运行继续爬去

`./phantomjs/` `phantomjs`的程序

`spider-log.log` 日志文件
