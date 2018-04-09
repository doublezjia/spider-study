#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-03-22 16:06:59
# @Author  : zealous (doublezjia@163.com)
# @Link    : https://github.com/doublezjia
# @Version : $Id$
# @Desc    : 拉钩python爬虫

import os,io,requests,sys,time,csv,random,json
from datetime import datetime
from pyecharts import *


# 请求头
headers = {
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Connection':'keep-alive',
'Content-Length':'25',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie':r'ga=GA1.2.679448833.1513931531; user_trace_token=20171222163110-76ae1cf8-e6f2-11e7-a521-525400f775ce; LGUID=20171222163110-76ae22b2-e6f2-11e7-a521-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521879218,1521881929,1521881944,1522047325; index_location_city=%E5%B9%BF%E5%B7%9E; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=3; gate_login_token=11155d8fa0e7f3f9592dbbc0040b0d08960610ab258f8f7e; JSESSIONID=ABAAABAAADEAAFI74C113D25E27F0546817D6B29C21AB3A; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522047881; _gat=1; _gid=GA1.2.1935285762.1522047325; LGSID=20180326145235-43967b49-30c2-11e8-9f3b-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20180326150151-8f4264b9-30c3-11e8-9f3c-525400f775ce; _putrc=""; login=false; unick=""; TG-TRACK-CODE=index_navigation; gate_login_token=""; SEARCH_ID=ad8071df4e624234b3f34cc0a60df259',
'Host':'www.lagou.com',
'Referer':r'https://www.lagou.com/jobs/list_Python?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
'X-Anit-Forge-Code':'0',
'X-Anit-Forge-Token':'None',
'X-Requested-With':'XMLHttpRequest'
}

# 地址
url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0'

# 用来显示
base_screen = '''
职    位 : {positionName}
经    验 : {workYear}
学历要求 : {education}
薪    酬 : {salary}
所在地区 : {city}-{district}
工作类型 : {firstType} {secondType}
公 司 名 : {companyFullName}
公司规模 : {companySize}
行    业 : {industryField}
福利优势 : {positionAdvantage}
发布时间 : {createTime}
职位 TAG : {positionLable}
公司 TAG : {companyLabel}
'''


#保存数据到csv文件
def save_csv(lgmsg):
	with open('lg-python-job.csv','a',newline='') as datacsv:
		csvwriter = csv.writer(datacsv,dialect=('excel'))
		csvwriter.writerow(lgmsg)


# 爬虫
def lagou_spider(num=1):

	# 请求表单
	dataform = {
	'first':'true',
	'kd':'Python',
	'pn':str(num)}


	# 发送请求
	req = requests.post(url,headers=headers,data=dataform)
	req.encoding = 'utf-8'
	if req.status_code == 200:
		# 把json转为字典
		data = json.loads(req.text)

		# 获取目标内容
		for item in data['content']['positionResult']['result']:
			positionName = item['positionName']
			workYear = item['workYear']
			education = item['education']
			salary = item['salary']
			city = item['city']
			district = item['district']
			firstType = item['firstType']
			secondType = item['secondType']
			companyShortName = item['companyShortName']
			companyFullName = item['companyFullName']
			companySize = item['companySize']
			industryField = item['industryField']
			positionAdvantage = item['positionAdvantage']

			createTime = item['createTime']

			positionLables = item['positionLables']
			positionLable = ''
			for plitem in positionLables:
				positionLable = positionLable + ' ' + plitem
			
			companyLabelList = item['companyLabelList']
			companyLabel = ''
			for clitem in companyLabelList:
				companyLabel =companyLabel + ' ' + clitem


			# 显示到屏幕上
			screenmsg = base_screen.format(
				positionName=positionName,workYear=workYear,
				education=education,salary=salary,city=city,
				district=district,firstType=firstType,secondType=secondType,
				companyFullName=companyFullName,companySize=companySize,
				industryField=industryField,positionAdvantage=positionAdvantage,
				createTime=createTime,positionLable=positionLable,companyLabel=companyLabel
				)
			print (screenmsg)

			# 保存数据到csv文件
			lgmsg = (positionName,workYear,education,salary,city,district,firstType,secondType,
				companyShortName,companyFullName,companySize,industryField,positionAdvantage,createTime,positionLable,
				companyLabel)
			save_csv(lgmsg)
	else:
		sys.exit('访问出错,退出运行')

	
	# 防止网站禁爬
	waitnum = random.randint(3,10)
	print ('防止网站禁爬，请等待 %s 秒' % waitnum)
	time.sleep(waitnum)
	print('本页结束，爬去下一页')



		

if __name__ == '__main__':

	print('\n拉勾网上发布的全国python职位招聘爬虫\n')

	# csv文件表格的头
	lg_csv_header = ('职位','经验','学历要求','薪酬','所在城市','所在区','工作类型1','工作类型2',
		'公司简称','公司全称','公司规模','行业','福利优势','发布时间','职位TAG','公司TAG')
	with open('lg-python-job.csv','w',newline='') as datacsv:
		csvwriter = csv.writer(datacsv,dialect=('excel'))
		csvwriter.writerow(lg_csv_header)


	# 爬虫开始时间
	print ('爬虫开始')
	start = datetime.now()
	for i in range(1,31):
		lagou_spider(i)

	# 爬虫结束时间
	end = datetime.now()
	# 计算时间相差,得到耗时
	tiemcount = end-start
	print('爬虫结束,耗时: %s' % tiemcount)