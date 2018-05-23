# 爬取拉勾网上全国Python招聘信息

本爬虫是爬取拉钩网上Python招聘信息保存到CSV中并结合pyecharts生成统计图表。

## 文件说明
- lagouspider.py 为爬虫脚本，用于爬取拉钩网上Python招聘信息保存到CSV中。
- readcsv.py 为统计数据脚本，结合pyecharts生成网页形式的图表。
- lg-python-job.csv 为爬虫数据保存的csv文件，通过爬虫脚本自动生成。
- render.html 为生成的图表的网页，通过统计数据脚本自动生成。
