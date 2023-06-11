# -*- coding: utf-8 -*
import Display as DISP
import ProcessImage as IMG  # imgProcess的简称


# 加载菜单页
def Start():
    """
    该函数用于加载菜单页，以开始整个进程
    :return: None
    """
    backImage = IMG.read("resource/Decorate.jpeg")
    DISP.ShowMenu(backImage)


# 创建九宫格图
def CreateNineGrid():
    """
    该函数用于调用TK的文件选择，并调用
    :return: OpenCV格式的9张图的列表
    """
    filePath = DISP.getImagePath()
    GridCreator = DISP.GridImage()
    ninePics = IMG.gridToNine(IMG.read(filePath), 3)
    GridCreator.showWindow(ninePics)


def Capture():
    filePath = DISP.getImagePath()
    Captureor = DISP.DragCapture()
    Captureor.showWindow(IMG.read(filePath))


# 为图片打马赛克
def CreateMosaicImg():
    filePath = DISP.getImagePath()
    MosaicCreator = DISP.MosaicImage()
    MosaicCreator.showWindow(IMG.read(filePath))


def AutoCreateMosaicImg():
    filePath = DISP.getImagePath()
    axis = IMG.locateFace(IMG.read(filePath))
    MosaicCreator = DISP.MosaicImage_Auto(axis=axis)
    MosaicCreator.showWindow(IMG.read(filePath))


# 为图像调整参数
def CreateAttributeImg():
    filePath = DISP.getImagePath()
    AttributeSetor = DISP.AttributeImage()
    AttributeSetor.showWindow(IMG.read(filePath))


def AutoAttributeImg():
    filePath = DISP.getImagePath()
    AttributeSetor = DISP.AttributeImage_Auto()
    AttributeSetor.showWindow(IMG.read(filePath))


def Exit():
    print("您已正常退出，感谢使用")
    exit(0)
