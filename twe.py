#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2019-02-15 09:57:25
# @Author  : zealous (doublezjia@163.com)
# @Link    : https://github.com/doublezjia
# @Version : $Id$
# @@Desc   :爬取猫眼流浪地球累计票房发送到邮箱

import os,sys,requests
from bs4 import BeautifulSoup
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


url = 'https://piaofang.maoyan.com/movie/248906?_v_=yes'
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
}
# 爬取累计票房
def main():
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text,'html.parser')
	title = soup.find('span',{'class':'info-title-content'}).text
	rating = soup.find('span',{'class':'rating-num'}).text
	data = soup.find_all('span',{'class':'detail-num'})
	img = soup.find('div',{'class','info-poster'}).img['src']
	cumulative_box_office = data[0].text
	forecast_box_office = data[3].text
	gap = float(forecast_box_office) - float(cumulative_box_office )
	last_update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	message = '''
	<p><img src='http://{img}'/></p>
	<p><h1>{title}</h1></p>
	<p>评分:{rating}分</p>
	-------------------------------------
	<p>内地票房 </p>
	<p>累计票房:{cumulative_box_office}亿</p>
	<p>预测票房:{forecast_box_office}亿</p>

	<p>距离预测票房还有{gap}亿</p>

	<p>最后更新时间:{last_update_time}</p>

	'''.format(title=title,rating=rating,
		cumulative_box_office=cumulative_box_office,
		forecast_box_office=forecast_box_office,gap=round(gap,2),
		img=img,
		last_update_time=last_update_time)

	# print (message)
	if float(cumulative_box_office) >= 50:
		message = '''
		<p><img src='http://{img}'/></p>
		<p>h1>{title}</h1></p>
		<p>评分:{rating}分</p>
		-------------------------------------
		<p>内地票房 </p>
		<H1>恭喜{title}票房超过50亿</H1>
		<p>累计票房:{cumulative_box_office}亿</p>
		<p>预测票房:{forecast_box_office}亿</p>

		<p>距离预测票房还有{gap}亿</p>

		<p>最后更新时间:{last_update_time}</p>

		'''.format(title=title,rating=rating,
			cumulative_box_office=cumulative_box_office,
			forecast_box_office=forecast_box_office,gap=round(gap,2),
			img=img,
			last_update_time=last_update_time)



	try:
		sendEmail(message,title,cumulative_box_office)
	except:
		with open('error.log','a') as f:
			f.write('[%s]send Email faild.' % datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
	
# 发送邮件
def sendEmail(msg,Movie_name,cumulative_box_office):
	sender = 'abc@qq.com'
	sender_pwd = '123456'
	receivers = 'abc@qq.com'

	message = MIMEText(msg,'html','utf-8')
	message['From'] = formataddr(["zealous",sender])
	message['TO'] = formataddr(["zealous",receivers])
	message['Subject'] = '%s当前累计票房%s亿' % (Movie_name,cumulative_box_office)

	server = smtplib.SMTP_SSL('smtp.qq.com',465)
	server.login(sender,sender_pwd)
	server.sendmail(sender,[receivers,],message.as_string())


if __name__ == '__main__':
	main()
