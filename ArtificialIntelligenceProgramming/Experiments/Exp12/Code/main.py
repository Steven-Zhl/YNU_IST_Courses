# -*- coding: utf-8 -*

"""
欢迎查看图片图片处理程序的源代码。
本程序大致引用的库如下：
后端：
图像处理主要基于OpenCV、numpy完成；少量使用PIL，其目的仅为图片格式转换；
前端：
界面框架基于tkinter搭建，采用了面向对象的设计思路，良好地实现了对重复组件的重写和复用。
其他：
(1)人脸定位基于cv2.CascadeClassifier()实现，使用了@vpisarev的训练集haarcascade_frontalface_default.xml
源文件地址：https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
(2)图像增强基于自动对比度和自动色阶算法实现，参考了以下文章后使用cv2和numpy重写。
①[Visual Basic实现]：https://www.cnblogs.com/Imageshop/archive/2011/11/13/2247614.html
②[Matlab实现]：https://blog.csdn.net/bluecol/article/details/45576827
(3)本程序设计时一定程度上借鉴了工厂模式，使用一个创建对象的接口（实为ControlPanel对象）实现对多种对象的创建
"""
import ControlPanel

ControlPanel.Start()
