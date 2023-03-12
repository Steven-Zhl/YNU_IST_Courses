#注：在python中需要注意代码之间的缩进，通常以一个tab的距离表示隶属关系

import os #1、利用import语句进行导入模块，用逗号分隔可以导入多个包
import math,copy,random,time
from collections import Counter  #2、利用from...import ....进行导入
import numpy as np  #3、利用as关键字重命名包名，以后再使用就可以直接用np了

def hello_world():  #4、利用def关键字创建函数，简单来说：函数就是将具有独立功能的代码块组织成一个模块，需要的时候调用
	#创建函数格式：def name(参数1，参数2....):
	yourname = input('你好，请输入你的名字:')  #5、输入函数，input(),若input中有字符串可以输出
	print('欢迎来到Python的世界,',yourname)  #6、输出函数,print()，若要输出多个对象，利用逗号分隔
	print('让我们开始学习吧~')

def hello_twice():
	global yourname,yourheight,yourweight  #7、利用global关键字定义全局变量，使之在整个程序运行周期能够被调用
	yourname = input('请输入你的名字：')
	yourheight = input('请输入你的身高:')
	yourweight = input('请输入你的体重:')

#python中字符串的部分操作
def deviding_line():
	word1 = 'i am line'  #8、字符串的创建，利用单引号' 或者双引号" 进行创建
	word2 = word1.upper()  #9、字符串的函数，利用运算符.进行调用，该语句中的upper()可以将字符串转换为全大写字母
	word3 = word1.lower()  #10、lower()函数，将字符串转换为全小写
	word4 = word1.title()  #11、title()函数，可以将字符串标题化
	#以上三个函数仅为字符串的部分函数
	words = [word1,word2,word3,word4]  #12、[]可以创建一个列表，列表可以存放很多的对象
	line = '-' * 40  #13、利用*运算符创建串，这里就是有40个-符号

	endReturn = line+words[random.randint(0,3)]+line #14、字符串可以利用+号直接相连
	#15、上面出现的random.randint()可以创建随机整数,0和3为随机数的上下限
	return endReturn  #16、函数返回值，可以在被调用时将这个值返回

#学习python中的数字模型
def study_number():
	num1 = input('请输入一个数字:')
	print('你输入的是数字%s'%num1,'可它的类型为：',type(num1)) #17、输出函数格式控制
	#18、type()函数可以返回该值的类型
	num2 = int(input('再输入一个数字:'))  #19、利用int()函数进行数值类型转换，将数字转换为int整型
	print('你输入的是数字%s' % num2, '它的类型为：', type(num2))
	num3 = float(input('再输入一个数字:'))  #20、float()函数可以转换为浮点数类型
	print('你输入的是数字%s' % num3, '它的类型为：', type(num3))
	print('num1+num2={}'.format(int(num1)+num2)) #21、数字加法
	# 22、format()函数格式化输出，在字符串中的{}符号将被替换为format()的参数
	print('num1-num2={}'.format(int(num1)-num2))   #23、数字减法
	print('num1*num2={}'.format(num1*num2)) #24、num1*num2并不会是你想要的数据，因为input()函数，默认输入为字符类型
	print('num1*num2={}'.format(int(num1) * num2))  #25、数字乘法
	print('num2//num3={:.3f}'.format(num2//num3)) #26、数字整除，同时{:.3f}表示输出格式小数点后面保留三位
	print('num2/num3={:.4f}'.format(num2/num3)) #27、数字除法，保留小数点后四位
	print('num2%num3={:.4f}'.format(num2 % num3)) #28、求余数
	print('num2%num3={:.4%}'.format(num2%num3)) #29、求余数，{:.4%}输出格式为百分比格式
	print('num1**num2={}'.format(int(num1)**num2))  #30、幂运算
	print('This is the {a},and {b}'.format(a='numbers',b='some operations')) #31、format多参数，标记位置对应输出

	one,two,three = True,True,False  #32、bool值
	print(one,two,three)
	print('and运算符:',one and two,one and three) #33、and运算，当两个值同时为真时才为真
	print('or运算符:',one or two,one or three) #34、or运算符，当两个值同假时为假
	print('not运算符:',not one,not two,not three)  #35、not运算符，得到相反的值

#学习python中的列表模型
def study_list(length): #36、带有参数的函数
	l1 = [1,2,3,4,5,9.0]   #37、创建列表，利用符号[]
	l2 = list(range(10,10+length))  #38、创建列表，也可以用list()
	#39、range()函数，可以创建一个整数列表，格式为range(start,end,step)，start为开始位置，end为结束位置，前闭后开，step为步长
	print('l1的类型为：',type(l1))
	print(l1[1],l2[1])  #40、访问列表值，可以直接用list[num]的方式进行访问
	l3 = l2  #41、将l2的引用赋给l3
	print(id(l1),id(l2),id(l3)) #42、id()函数可以获取对象的内存地址，在这里可以看到l3的的地址和l2是一样的
	l3[0]=99  #43、更新列表值
	print('l2==l3么?',l2==l3)   #44、更新l3后依旧等于l2，因为l3和l2本来就是一个对象，不过换了个名字
	l4 = l2.copy()  #45、复制一个l2给l4，copy()创建一个一模一样的列表
	l4[0]=999
	print('l4==l2么?',l4==l2)  #46、此时l4不等于l2
	print('删除前',l4)
	del l4[0]  #47、del语句进行删除列表值，在python中del可以删除所有的变量
	print('删除后',l4)
	l4.append(30)  #48、给列表添加值
	l4.extend(l1)  #49、给列表追加一个序列多个值
	print('添加l1后:',l4)
	l4.reverse()  #50、列表反转
	print('反转后:',l4)
	l4.sort()  #51、sort()函数，将列表进行排序
	print('排序后:',l4)

#学习python中的元组模型
def study_tuple(length:int)->bool:  #52、解释参数类型的函数创建，->为返回值类型
	tuple1 = (1,2,3,4)  #53、创建元组，利用()符号，元组的特性是不可以改变
	tuple2 = tuple(range(10,10+length))  #54、利用tuple创建元组

	print(tuple1.count(1))  #55、元组函数count(),用于输出某个值的数量
	print(tuple1.index(1)) #56、元组函数index(),可以按照索引得到值
	try:    #57、python中的异常处理，try:语句内部如果出现错误则会转入到except中
		tuple1[0] = 9  #58、因为元组的不可改变性，所以该语句会出错
	except TypeError:
		print('元组插入失败')
	finally:  #59、finally内语句不管是否出现错误都会执行
		print('不管插入成不成功我都会执行')

	try:
		print(id(tuple1),id(tuple2))
	except:
		return False
	else:
		tuple3 = tuple1+tuple2  #60、元组虽然不可改变，但是可以通过+号进行合并为另一个元组
		print(tuple3,id(tuple3))
	return True

def study_dict():  #学习python中的字典模型，字典是  键->值 的映射
	dict1 = {1:'一',2:'二',3:'三',4:'四'}  #61、以下为创建字典的5种方法
	dict2 = dict(one=1,two=2,three=3)
	dict3 = dict(zip([6,7,8,9],['Six','Seven','Eight','Nine']))
	dict4 = dict([('One',1),('Two',2),('Three',3)])
	dict5 = dict({1:'一',2:'二',3:'三',4:'四'})
	print(type(dict1),dict1==dict5)  #62、可以看到，dict1和dict5是等价的
	print(dict1[1],dict2['one'],dict3[6],dict4['One'],dict5[1])  #63、通过字典的键访问
	print(dict1.get(4)) #64、通过get函数访问内容

	dict1[1] = '壹' #65、修改字典内容
	dict1[5] = '五' #66、添加字典
	print(dict1)
	print(1 in dict1, 6 in dict1, 7 not in dict1) #67、in和not in关键字，可以判断值是否在序列中
	dict6 = dict1.copy()  #68、字典的复制
	dict6[1] = 'One'
	print(dict1,'<dict1------------dict6>',dict6)

	dict1.clear() #69、字典的清空
	print(dict1)
	del dict1,dict2,dict3,dict4,dict5,dict6 #70、删除字典,也可以用del dict[key]的方式删除某个键

def study_set(): #python中集合的学习，集合中不存在相等的值
	set1 = set(['You','Are','Not','Beautiful']) #71、利用set()函数进行创建集合
	set2 = {'You','Are','So','Beautiful'}  #72、利用{}创建集合，创建空集合的时候不能用{},因为{}表示字典
	set3 = set2.copy() #73、集合的复制

	print(type(set1))
	print(set1,set2)
	print(set1|set2)  #74、集合或运算符，得到两个集合中所有元素
	print(set1&set2)  #75、集合与运算符，得到两个集合共同元素
	print(set1^set2)  #76、不同时包含于set1和set2的元素
	print(set1-set2)  #77、集合差运算，得到set1有，set2没有的元素
	print(set1<=set2,set3<=set2,set3<set2)  #78、<=符号，判断是否为子集，<符号，判断是否为真子集


	set1.add('Me too') #79、集合添加元素
	print('is语句用法',set3==set2,set3 is set2,set1 is not set2) #80、is和is not语句，is语句用于判断对象是否一样，==判断值是否一样
	set3.clear()  #81、清空集合，集合变为空
	print(set3)
	del set3

def study_Some_functions(): #python中一些函数
	list1 = [1,2,3,4,5,6]  #同学们，眼熟不，这就是之前的列表，下面的这些大家都认认是啥
	tuple1 = (11,12,13,14,15,16)  #元组
	set1 = set(list1)  #集合
	dict1 = dict(zip([1,2,3,4,5],['one','Two','Three','Four','Five']))  #字典

	print(max(list1),max(tuple1),max(set1),max(dict1))  #82、max()函数，得到序列中最大值
	print(min(list1),min(tuple1),min(set1),min(dict1))  #83、min()函数，得到最小值
	print(sum(list1),sum(tuple1),sum(set1),sum(dict1))  #84、sum()函数，得到序列和
	print(len(list1),len(tuple1),len(set1),len(dict1))  #85、len()函数，得到序列长度
	print(divmod(list1[0],tuple1[0]))  #86、divmod()函数，计算两个数的商和余数，结果两个格式为(商，余数)
	print(list(enumerate(tuple1)))  #87、enumerate()，给元组添加一个索引

	list2 = list(tuple1)  #88、利用list()将元组，字典等等转换为列表
	list3 = list(set1)
	list4 = list(dict1)
	tuple2 = tuple(list1)  #89、利用tuple()将列表，字典等转换为元组

	print(list2,list3,list4)

	for i in range(len(list1)):  #90、for循环语句
		print(list1[i],end=' ')  #91、print的属性end，可以使输出格式为end的内容，而不是默认换行
	print()
	for i in dict1:  #92、for循环遍历
		print(i,dict1[i],end=' ')

	list5 = list(reversed(list1))  #93、reversed()函数，可以反转序列
	print('\n',list5)  #94、\n,换行符

	testStr = "The mountains and rivers are different, the wind and the moon are the same"
	words = testStr.split(' ')  #95、split()函数，以split()内参数分割字符串，返回一个列表
	print(words)
	words.sort(key=len)  #96、sort()函数，进行排序，参数key=len时，以字符串长度为标准排序
	print('以长度排序:',words)
	words.sort(key=len, reverse=True)  #97、reverse参数，结果反转
	print('以长度排序并且反转:', words)
	words.sort(key=str)  #98、以字典序进行排序
	print('以字典序排序:',words)

	ct = Counter(testStr)  #99、collections模块中的Counter,可以得到字符串中每个数字出现次数
	print(ct)
	ct.update('eeeexxxxxlllll')  #100、更新
	print(ct)
	print(ct.most_common(5))  #101、得到字符数最多的前五位

def study_Slice():  #python的切片操作，得到序列的部分内容
	str1 = 'I hope one day, I can find you, my sweet dream'
	list1 = list(range(10))
	tuple1 = tuple(list1)

	print(str1[:])  #102、切片格式为str[start:end:step]，前闭后开,step可为正负，默认步长为1
	print(str1[::-1])  #103、当步长为负数的时候，反转
	print(str1[:15])  #104、只有end时，截取最开始到end
	print(str1[15:])  #105、只有start时，截取从start到末尾的所有字符
	print(str1[::2])  #106、步长为2
	print(str1[1::2])

	print(list1[:])  #107、和str一样
	print(list1[2:])
	print(list1[:2])
	print(list1[::-1])

	list1[1:5] = [10] #切片赋值，右边必须为一个可以遍历的序列
	#list1[1:5] = 10   这样就会报错
	print(list1)

def study_loop_select():  #python中的循环和选择语句
	list1 = [1,2,3,4,5]
	num = int(input('while循环，输入你想要循环的次数:'))
	i = 1
	while i<=num:  #108、while expression:当expression为真的时候进行循环
		if i<5:  #109、if...elif...else选择语句，如果判断结果只有两个,可以使用if...else
			print('我打印了',i,'次')
		elif i<10:
			print('打印了',i,'次，真累啊')
		elif i<15:
			print('打印太多啦,再打印我就要停止了...')
		elif i<20:
			print('continue...')
			i+=1
			continue   #110、continue语句，用在循环中，continue后的所有语句都不允许，直接进入下次循环
			print('我想我可能输出不了了')
		else:
			print('累死我了，休息。都',i,'次了~_~')
			break  #111、break语句，运用在循环中，直接退出循环，所以，在本例子中，这个循环最多循环20次
		i+=1
		time.sleep(0.5)  #112、time库为python中的时间库，time.sleep(second)可以使程序暂停运行second秒
	else:  #113、while循环后接一个else语句，当执行完所有循环后执行一次，可以省略(个人感觉用处不大)
		print('while结束了')

	for i in list1:   #113、for循环，上面代码有用到过
		print(i,end=' ')
	print()
	for i in range(5):
		print(i)


def study_expression_deduction(): #114、python表达式推导
	list1 = [i for i in range(10)]   #115、利用该语句推导出列表
	list2 = [x for x in range(20) if x%2==0]  #116、语句中增加if，满足if后表达式的才会是列表
	print(list1,'<list1--------------list2>',list2)

	print(deviding_line())  #117、函数可以在任何地方被调用，如果是自己调用自己就可以称为递归调用

	list3 = [['_'] * 3 for i in range(3)]
	print(list3)

	fruits = ['Apple','Banana','Pear']
	colors = ['Red','Yellow','Green']
	suitcolor = [(color,fruit) for color,fruit in zip(colors,fruits)] #118、两个列表合并
	print(suitcolor)
	cartesian = [(color,fruit) for color in colors for fruit in fruits] #119、两个列表的笛卡尔积
	print(cartesian)

	dict1 = {fruit:color for fruit,color in suitcolor}  #120、字典的推导，只要是带有键值对的任何序列，都可以推导出字典
	print(dict1)

def study_files():
	filepath = input('请输入你的文件路径（输入quit退出）:')
	if filepath=='quit':
		return True
	try:
		file = open(filepath,'w') #121、打开文件，'w'为写格式打开
		file.write('哈哈，现在开始写文件')  #122、向文件写入字符串
		file.close()  #123、关闭文件
		file = open(filepath,'r')  #122、以'r'读格式打开
		print('从文件中读出的内容：\n',file.read())  #123、read()函数可以得到文件内容
	except FileNotFoundError:
		print('文件未找见请重新输入')
		study_files()  #124、这就是上面所说的递归调用
	except:
		print('出现错误,请重新输入路径')
		study_files()

class Users():  #125、面向对象编程，python中创建类class，类包含有属性与方法，包括有私有变量，共有变量等等
	def __init__(self,name,height,weight):  #126、类的构造方法，创建实例时自动调用
		self.name = name
		self.height = height
		self.weight = weight
		self.yanzhi = 100

	def display(self): #127、类方法
		print('大家好，我是{},身高{},体重{},颜值超高{}'.format(self.name,self.height,self.weight,self.yanzhi))

if __name__=="__main__":  #128、无论之前有什么，程序都会从这里开始运行
	hello_world()  #129、所以这是运行的第一句，调用该函数
	deviding_line()
	try:
		print(yourname)  #130、调用完hello_world()函数后，因为在hello_world()函数内部有一个yourname变量，所以我们进行输出，看在这里能不能找见这个变量
	except:
		print('  未能找见该变量  ')#131、不可能找见这个变量的，因为yourname是局部变量，只存在于hello_world()函数内部
	deviding_line()
	hello_twice()  #132、因为在该函数中定义了global语句，所以该函数中的变量在以下程序中都可以使用

	user = Users(yourname,yourheight,yourweight) #133、实例化对象，创建Users类的实例
	user.display()  #134、对象调用方法

	#135、在python中，可以用三引号进行多行注释，但是如果用变量接收注释的话也可以是一个有格式的字符串，如下
	chooseinformation = '''Input the number of the function you want to Run(quit is exit):
	1、study_number		2、study_list
	3、study_tuple		4、study_dict
	5、study_set			6、study_Some_functions
	7、study_Slice		8、study_loop_select
	9、study_expression_deduction
	10、study_files		
	'''
	deviding_line()
	while True: #136、while循环进行运行程序，只有当输入quit时才会退出循环(不过你强制退出当然也可以退出)
		input('按键继续') #137、为了让输出不那么快，等待按键后才输出以下内容
		print(chooseinformation)
		num = input('输入序号:')
		#138、在以下if...elif...else选择中，我们来选择运行不同的函数
		if num=='quit':
			break
		elif num=='1':
			study_number()
		elif num=='2':
			study_list(10)
		elif num=='3':
			study_tuple(10)
		elif num=='4':
			study_dict()
		elif num=='5':
			study_set()
		elif num=='6':
			study_Some_functions()
		elif num=='7':
			study_Slice()
		elif num=='8':
			study_loop_select()
		elif num=='9':
			study_expression_deduction()
		elif num=='10':
			study_files()
		deviding_line()
	print('哈哈，恭喜你，这个程序结束咯~')



