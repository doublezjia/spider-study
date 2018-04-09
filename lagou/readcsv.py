#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 16:20:34
# @Author  : zealous (doublezjia@163.com)
# @Link    : https://github.com/doublezjia
# @Version : $Id$
# @Desc    : 统计从拉勾网上爬去的python的招聘信息

import os,csv,sys
from pyecharts import *


# 省份地区列表
province = [{'sub': [], 'province': '北京'}, {'sub': ['广州', '深圳', '珠海', '汕头', '韶关', '佛山', '江门', '湛江', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮'], 'province': '广东'}, {'sub': [], 'province': '上海'}, {'sub': [], 'province': '天津'}, {'sub': [], 'province': '重庆'}, {'sub': ['沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦', '铁岭', '朝阳', '葫芦岛'], 'province': '辽宁'}, {'sub': ['南京', '苏州', '无锡', '常州', '镇江', '南通', '泰州', '扬州', '盐城', '连云港', '徐州', '淮安', '宿迁'], 'province': '江苏'}, {'sub': ['武汉', '黄石', '十堰', '荆州', '宜昌', '襄樊', '鄂州', '荆门', '孝感', '黄冈', '咸宁', '随州', '恩施土家族苗族自治州', '仙桃', '天门', '潜江', '神农架林区'], 'province': '湖北'}, {'sub': ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', '巴中', '资阳', '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州'], 'province': '四川'}, {'sub': ['西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛'], 'province': '陕西'}, {'sub': ['石家庄', '唐山', '秦皇岛', '邯郸', '邢台', '保定', '张家口', '承德', '沧州', '廊坊', '衡水'], 'province': '河北'}, {'sub': ['太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁'], 'province': '山西'}, {'sub': ['郑州', '开封', '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌', '漯河', '三门峡', '南阳', '商丘', '信阳', '周口', '驻马店', '焦作'], 'province': '河南'}, {'sub': ['长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延边朝鲜族自治州'], 'province': '吉林'}, {'sub': ['哈尔滨', '齐齐哈尔', '鹤岗', '双鸭山', '鸡西', '大庆', '伊春', '牡丹江', '佳木斯', '七台河', '黑河', '绥化', '大兴安岭地区'], 'province': '黑龙江'}, {'sub': ['呼和浩特', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '锡林郭勒盟', '兴安盟', '阿拉善盟'], 'province': '内蒙古'}, {'sub': ['济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照', '莱芜', '临沂', '德州', '聊城', '滨州', '菏泽'], 'province': '山东'}, {'sub': ['合肥', '芜湖', '蚌埠', '淮南', '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '巢湖', '六安', '亳州', '池州', '宣城'], 'province': '安徽'}, {'sub': ['杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水'], 'province': '浙江'}, {'sub': ['福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德'], 'province': '福建'}, {'sub': ['长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州', '永州', '怀化', '娄底', '湘西土家族苗族自治州'], 'province': '湖南'}, {'sub': ['南宁', '柳州', '桂林', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左'], 'province': '广西'}, {'sub': ['南昌', '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶'], 'province': '江西'}, {'sub': ['贵阳', '六盘水', '遵义', '安顺', '铜仁地区', '毕节地区', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州'], 'province': '贵州'}, {'sub': ['昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱', '临沧', '德宏傣族景颇族自治州', '怒江傈僳族自治州', '迪庆藏族自治州', '大理白族自治州', '楚雄彝族自治州', '红河哈尼族彝族自治州', '文山壮族苗族自治州', '西双版纳傣族自治州'], 'province': '云南'}, {'sub': ['拉萨', '那曲地区', '昌都地区', '林芝地区', '山南地区', '日喀则地区', '阿里地区'], 'province': '西藏'}, {'sub': ['海口', '三亚', '五指山', '琼海', '儋州', '文昌', '万宁', '东方', '澄迈县', '定安县', '屯昌县', '临高县', '白沙黎族自治县', '昌江黎族自治县', '乐东黎族自治县', '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县'], 'province': '海南'}, {'sub': ['兰州', '嘉峪关', '金昌', '白银', '天水', '武威', '酒泉', '张掖', '庆阳', '平凉', '定西', '陇南', '临夏回族自治州', '甘南藏族自治州'], 'province': '甘肃'}, {'sub': ['银川', '石嘴山', '吴忠', '固原', '中卫'], 'province': '宁夏'}, {'sub': ['西宁', '海东地区', '海北藏族自治州', '海南藏族自治州', '黄南藏族自治州', '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州'], 'province': '青海'}, {'sub': ['乌鲁木齐', '克拉玛依', '吐鲁番地区', '哈密地区', '和田地区', '阿克苏地区', '喀什地区', '克孜勒苏柯尔克孜自治州', '巴音郭楞蒙古自治州', '昌吉回族自治州', '博尔塔拉蒙古自治州', '石河子', '阿拉尔', '图木舒克', '五家渠', '伊犁哈萨克自治州'], 'province': '新疆'}, {'sub': [], 'province': '香港'}, {'sub': [], 'province': '澳门'}, {'sub': [], 'province': '台湾'}, {'sub': [], 'province': '海外'}]


# 读取csv表内容
def read_csv():
	if os.path.isfile('lg-python-job.csv'):
		with open('lg-python-job.csv','r') as csvf:
			reader = csv.reader(csvf)
			rows = [row for row in reader]
			return rows
	else:
		sys.exit('没有csv文件,请先运行 lagouspider.py 爬去数据，生成csv')


# 生成地图表格
def map_echart():
	# 获取csv数据
	rows= read_csv()
	# 统计表中同一城市的招聘数量用的字典
	citydict={}
	# 统计省份的招聘数量用的字典
	prodict = {}
	# 这两个是生成表格时候用的
	value = []
	attr = []
	map1 = Map('拉钩网上python招聘全国分布',width=1200,height=600,title_pos='center')
	# 统计表中同一城市的招聘数量
	for i in range(len(rows)):
		if i > 0:
			city = rows[i][4]
			if city in citydict:
				citydict[city]=citydict[city] + 1
			else:
				citydict[city]=1		

	# 把表中的城市按省份分布
	# 统计省份的招聘数量
	for item in province:
		provnum = 0;
		# 判断city是否是属于省份还是直辖市
		# 循环城市字典
		for cityitem in citydict:
			# 如果是直辖市的
			if cityitem == item['province']:
				# 统计数据并放在Prodict字典中
				provnum = provnum + citydict[cityitem]
				prodict[cityitem] = provnum
			# 如果不是直辖市的
			else:
				# 判断城市是否在这个省份中
				if cityitem in item['sub']:
					provnum = provnum + citydict[cityitem]
					prodict[item['province']] = provnum
	# 把prodict字典中的值分别添加到attr和value列表中，用于生成图表
	for prokey in prodict:
		attr.append(prokey)
		value.append(prodict[prokey])
	# 生成地图
	map1.add("", attr, value, maptype='china',is_visualmap=True,visual_text_color='#000')
	return map1


# 各个城市比例
def city_echart():
	rows = read_csv()
	pie = Pie('拉钩网上python招聘的城市比例',width=1200,height=600,title_pos='center')
	citydict={}
	# 统计表中同一城市的招聘数量
	for i in range(len(rows)):
		if i > 0:
			city = rows[i][4]
			if city in citydict:
				citydict[city]=citydict[city] + 1
			else:
				citydict[city]=1
	# 生成图表
	attr=[];v1=[]
	for value in citydict:
		attr.append(value)
		v1.append(citydict[value])
	pie.add('',attr,v1,radius=[0,45],is_label_show=True,legend_pos='left',legend_orient='vertical')
	return pie

# 工作年限比例
def workyear_echart():
	rows = read_csv()
	pie = Pie('拉钩网上python招聘的工作年限比例',width=1200,height=600,title_pos='center')
	wydict={}
	# 统计表中工作年限数量
	for i in range(len(rows)):
		if i > 0:
			wy = rows[i][1]
			if wy in wydict:
				wydict[wy]=wydict[wy] + 1
			else:
				wydict[wy]=1	
	# 生成图表
	attr=[];v1=[]
	for value in wydict:
		attr.append(value)
		v1.append(wydict[value])	
	pie.add('',attr,v1,radius=[0,45],is_label_show=True,legend_pos='left',legend_orient='vertical')
	return pie

# 教育程度比例
def edu_echart():
	rows = read_csv()
	pie = Pie('拉钩网上python招聘的教育程度比例',width=1200,height=600,title_pos='center')
	edudict={}
	# 统计表中教育程度数量
	for i in range(len(rows)):
		if i > 0:
			edu = rows[i][2]
			if edu in edudict:
				edudict[edu]=edudict[edu] + 1
			else:
				edudict[edu]=1	
	# 生成图表
	attr=[];v1=[]
	for value in edudict:
		attr.append(value)
		v1.append(edudict[value])	
	pie.add('',attr,v1,radius=[0,45],is_label_show=True,legend_pos='left',legend_orient='vertical')
	return pie	

# 工资比例
def salary_echart():
	rows = read_csv()
	pie = Pie('')
	salarydict={}
	for i in range(len(rows)):
		if i > 0:
			salary = rows[i][3]
			if salary in salarydict:
				salarydict[salary]=salarydict[salary] + 1
			else:
				salarydict[salary]=1	
	attr=[];v1=[]
	for value in salarydict:
		attr.append(value)
		v1.append(salarydict[value])	
	pie.add('',attr,v1,radius=[0,45],is_label_show=True,legend_pos='left',legend_orient='vertical')
	return pie	

# 生成表格
def page_echart():
	page = Page()
	edu = edu_echart()
	city = city_echart()
	workyear = workyear_echart()
	map1 = map_echart()
	page.add(map1)
	page.add(city)
	page.add(edu)
	page.add(workyear)
	page.render()

if __name__ == '__main__':
	print ('统计表格')
	page_echart()
	print ('统计结束，可以点击render.html查看')