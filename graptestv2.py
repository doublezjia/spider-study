import random
import pygal

# 生产随机数
num = []
for i in range(20):
	a = random.randint(1, 10)
	num.append(a)


# 统计随机数出现的次数
num2 = []
for i in num:
	b = num.count(i)
	num2.append(b)



# 对结果进行可视化
hist = pygal.Bar()      # 生成实例
hist.title = 'random test'  # 标题

# X轴数值坐标
hist.x_labels = map(str,range(20))


hist.x_title = 'random num'                  # X轴标题
hist.y_title = 'random count'                # Y轴标题
 
hist.add('random count',num2)                # 传入Y轴数据
hist.render_to_file('random_conunt.svg')     # 文件生成路径，必须为svg格式文件