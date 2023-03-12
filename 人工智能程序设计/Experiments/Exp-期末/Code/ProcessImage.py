# -*- coding: utf-8 -*
"""
本程序主要负责对OpenCV的图像对象进行处理、转换
因为其操作过程不需要全局变量，故采用面向过程的编程思路
使用须知：
(1)由于OpenCV库不支持中文（无论是否UTF-8），所以请保证操作过程中路径名、文件名以及其他与cv2库函数有关的内容不包含中文
(2)由于使用cv2.CascadeClassifier时，参数需要为绝对路径，所以请在运行时手动修改函数locateFace内的路径
"""
import cv2 as cv
import numpy as np
from PIL import Image, ImageEnhance

__all__ = ['read', 'save', 'capturePart', 'gridToNine', 'addMosaic', 'enhance', 'locateFace', 'autoEnhance', 'find',
           'linearMap']


# 读取文件
def read(path):
    """
    该函数包装了cv2.imread()函数，使得看起来美观一些
    :param path:图片的绝对路径
    :return:openCV读取的图片矩阵
    """
    return cv.imread(path)


# 保存文件
def save(image_CV, path_dir, quality, name):
    """
    该函数通过传入的参数，将图片按照参数要求进行另存
    提示：命名不允许含有中文
    :param name: 被另存文件的名称
    :param image_CV: 被保存的图片或图片列表（OpenCV格式）
    :param path_dir: 所选目录的绝对路径
    :param quality: 保存质量。“Origin”-原画质；“High”-高画质；“Medium”；中画质；“Low”；低画质
    :return: None
    """
    if isinstance(image_CV, list):
        for i in range(len(image_CV)):
            path_save = path_dir + '/' + \
                (('Untitle_' if name == '' else (name + "_")) + str(i + 1)) + '.jpg'
            if quality == 'Origin':
                cv.imwrite(path_save, image_CV[i],
                           (cv.IMWRITE_JPEG_QUALITY, 100))
            elif quality == 'High':
                cv.imwrite(path_save, image_CV[i],
                           (cv.IMWRITE_JPEG_QUALITY, 72))
            elif quality == 'Medium':
                cv.imwrite(path_save, image_CV[i],
                           (cv.IMWRITE_JPEG_QUALITY, 60))
            elif quality == 'Low':
                cv.imwrite(path_save, image_CV[i],
                           (cv.IMWRITE_JPEG_QUALITY, 45))
    else:
        path_save = path_dir + '/' + \
            ('Untitle' if name == '' else name) + '.jpg'
        if quality == 'Origin':
            cv.imwrite(path_save, image_CV, (cv.IMWRITE_JPEG_QUALITY, 100))
        elif quality == 'High':
            cv.imwrite(path_save, image_CV, (cv.IMWRITE_JPEG_QUALITY, 72))
        elif quality == 'Medium':
            cv.imwrite(path_save, image_CV, (cv.IMWRITE_JPEG_QUALITY, 60))
        elif quality == 'Low':
            cv.imwrite(path_save, image_CV, (cv.IMWRITE_JPEG_QUALITY, 45))


# 截取子图
def capturePart(image_CV, boundary):
    """
    该函数将返回参数图片的坐标部分
    :param image_CV:OpenCV格式的图片
    :param boundary:各维度的边界，分别是[x左边界, x右边界, y上边界, y下边界]
    :return:经过截取后的新的图像
    """
    x_left = 0 if boundary[0] < 0 else boundary[0]
    x_right = image_CV.shape[1] - \
        1 if boundary[1] > image_CV.shape[1] - 1 else boundary[1]
    y_top = 0 if boundary[2] < 0 else boundary[2]
    y_bottom = image_CV.shape[0] - \
        1 if boundary[3] > image_CV.shape[0] - 1 else boundary[3]
    image_new_CV = image_CV[y_top:y_bottom, x_left:x_right]
    return image_new_CV


# 自动生成九宫格
def gridToNine(image_CV, blockNum_inRow):
    """
    该函数将参数图片平均切分为n^2块，并将其按行存入列表并返回
    :param image_CV:OpenCV格式的图像
    :param blockNum_inRow:一行的子块的个数
    :return:分割好的图像列表（按照行序存储）
    """
    height_origin = image_CV.shape[0]
    width_origin = image_CV.shape[1]
    height_block = height_origin // blockNum_inRow
    width_block = width_origin // blockNum_inRow
    images_grid = []
    for i in range(0, blockNum_inRow):
        for j in range(0, blockNum_inRow):
            boundary = [
                j * width_block, (j + 1) * width_block, i * height_block, (i + 1) * height_block]
            images_grid.append(capturePart(image_CV, boundary))
    return images_grid


# 创建马赛克图片
def addMosaic(image_CV, boundary, strength):
    """
    该函数接收原图片，在指定区域内按预设强度打码，并返回打码后的图片
    :param image_CV:OpenCV格式的图片
    :param boundary:各维度的边界，分别是[x左边界, x右边界, y上边界, y下边界]
    :param strength:马赛克强度，即单个色块的边长
    :return:添加马赛克后的图片
    """
    mosaicPart_height = boundary[3] - boundary[2]  # 马赛克区域的高度
    mosaicPart_width = boundary[1] - boundary[0]  # 马赛克区域的宽度
    mosaicImage = image_CV.copy()
    if strength != 0 and strength != 1:  # 当strength==0或==1时，将视为不进行马赛克处理
        for i in range(0, mosaicPart_width // strength + 1):
            for j in range(0, mosaicPart_height // strength + 1):
                leftEdge = boundary[0] + i * strength
                rightEdge = min(boundary[0] + (i + 1)
                                * strength, image_CV.shape[1] - 1)
                topEdge = boundary[2] + j * strength
                bottomEdge = min(boundary[2] + (j + 1)
                                 * strength, image_CV.shape[0] - 1)
                part_image = image_CV[topEdge:bottomEdge,
                                      leftEdge:rightEdge]  # 获取被打码部分的子图，用于计算颜色均值
                avg_color = np.average(np.average(
                    part_image, axis=0), axis=0)  # 先计算每行的均值，再计算总的均值
                mosaicImage[topEdge:bottomEdge,
                            leftEdge: rightEdge] = avg_color  # 填色
    return mosaicImage


# 返回调整参数后的文件
def enhance(image_CV, strength):
    """
    该函数利用PIL库，对OpenCV图片分为四部分，分别进行参数调整并返回拼合后的新图像
    :param image_CV:OpenCV格式的图像
    :param strength:强度列表，依次是亮度、色度、对比度、锐度；每个的范围应控制在[-4,4]之间，精度控制在1位
    :return:经调整后的拼合图像
    """
    height_block = image_CV.shape[0] // 2
    width_block = image_CV.shape[1] // 2
    # 截取并将其转化为可调整的对象
    image_brightPart = Image.fromarray(cv.cvtColor(
        image_CV[0:height_block - 1, 0:width_block - 1], cv.COLOR_BGR2RGBA))
    image_colorPart = Image.fromarray(
        cv.cvtColor(image_CV[0:height_block - 1, width_block:2 * width_block - 1], cv.COLOR_BGR2RGBA))
    image_contrastPart = Image.fromarray(
        cv.cvtColor(image_CV[height_block:2 * height_block - 1, 0:width_block - 1], cv.COLOR_BGR2RGBA))
    image_sharpPart = Image.fromarray(
        cv.cvtColor(image_CV[height_block:2 * height_block - 1, width_block:2 * width_block - 1], cv.COLOR_BGR2RGBA))
    # 调整并转化为OpenCV图片对象
    image_brightened = ImageEnhance.Brightness(
        image_brightPart).enhance(strength[0] + 1)  # 将Image对象转换为可调整对象
    image_brightened_CV = cv.cvtColor(np.asarray(
        image_brightened), cv.COLOR_RGB2BGR)  # 将其转换为OpenCV对象
    image_colored = ImageEnhance.Color(
        image_colorPart).enhance(strength[1] + 1)  # 调整亮度后的可调整对象
    image_colored_CV = cv.cvtColor(np.asarray(
        image_colored), cv.COLOR_RGB2BGR)  # 将其转换为OpenCV对象
    image_contrasted = ImageEnhance.Contrast(
        image_contrastPart).enhance(strength[2] + 1)  # 调整亮度后的可调整对象
    image_contrasted_CV = cv.cvtColor(np.asarray(
        image_contrasted), cv.COLOR_RGB2BGR)  # 将其转换为OpenCV对象
    image_sharped = ImageEnhance.Sharpness(
        image_sharpPart).enhance(strength[3] + 1)  # 调整亮度后的可调整对象
    image_sharped_CV = cv.cvtColor(np.asarray(
        image_sharped), cv.COLOR_RGB2BGR)  # 将其转换为OpenCV对象
    # 将图片按照对应位置赋值
    image_enhanced = np.zeros(
        (image_CV.shape[0], image_CV.shape[1], 3), np.uint8)
    image_enhanced[0:height_block - 1, 0:width_block - 1] = image_brightened_CV
    image_enhanced[0:height_block - 1, width_block -
                   1:2 * width_block - 2] = image_colored_CV
    image_enhanced[height_block - 1:2 * height_block -
                   2, 0:width_block - 1] = image_contrasted_CV
    image_enhanced[height_block - 1:2 * height_block - 2,
                   width_block - 1:2 * width_block - 2] = image_sharped_CV
    return image_enhanced


# 借助已有的数据集，定位人脸
def locateFace(image_CV):
    """
    该函数通过已训练好的训练集，定位OpenCV图像中人脸的位置
    PS：需要根据数据集的实际位置设定cv2.CascadeClassifier()的路径参数
    :param image_CV: OpenCV的图像
    :return: 人脸的位置坐标元组，分别是(左上顶点的x、y、宽度，高度)
    """
    face_cascade = cv.CascadeClassifier(
        "C:\\Users\\Steven\\PycharmProjects\\imgProcess\\resource\\haarcascade_frontalface_default.xml")
    grayImg = cv.cvtColor(image_CV, cv.COLOR_BGR2GRAY)
    location_face = face_cascade.detectMultiScale(
        grayImg, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))
    return location_face  # 返回的参数是一个元组，每个元组都有四个元素，分别为左上顶点的x、y、宽度，高度


def autoEnhance(image_CV, lowCut=0.005, highCut=0.005):
    """
    该函数实现了自动对比度、色阶算法
    :param image_CV: OpenCv格式的图像
    :param lowCut: 映射范围阈值
    :param highCut: 映射范围阈值
    :return: 增强后的图像
    """
    image_enhanced = image_CV.copy()
    height = image_CV.shape[0]
    width = image_CV.shape[1]
    pixelAmount = width * height
    histB = np.histogram(image_CV[:, :, 0], 256, [0, 256])[0]
    histG = np.histogram(image_CV[:, :, 1], 256, [0, 256])[0]
    histR = np.histogram(image_CV[:, :, 2], 256, [0, 256])[0]
    cumB = histB.cumsum()
    cumG = histG.cumsum()
    cumR = histR.cumsum()
    minB = find(cumB, pixelAmount * lowCut)
    minG = find(cumG, pixelAmount * lowCut)
    minR = find(cumR, pixelAmount * lowCut)

    maxB = find(cumB, pixelAmount * (1 - highCut))
    maxG = find(cumG, pixelAmount * (1 - highCut))
    maxR = find(cumR, pixelAmount * (1 - highCut))

    RedMap = linearMap(minR, maxR)
    GreenMap = linearMap(minG, maxG)
    BlueMap = linearMap(minB, maxB)
    for i in range(0, height):
        for j in range(0, width):
            image_enhanced[i, j, 0] = BlueMap[image_CV[i, j, 0]]
            image_enhanced[i, j, 1] = GreenMap[image_CV[i, j, 1]]
            image_enhanced[i, j, 2] = RedMap[image_CV[i, j, 2]]
    return image_enhanced


def find(tuple_input, limitation):
    """
    此函数被autoEnhance函数调用，用于查找元组中最先满足达到limitation的序号
    （由于np.where()不能完全替代Matlab中的find()函数，而用列表生成式会有很大的性能损失，所以设计这么个函数）
    :param tuple_input: 被遍历的元组
    :param limitation: 截止的限制值
    :return:满足条件的元素的序号
    """
    for i in range(len(tuple_input)):
        if tuple_input[i] >= limitation:
            return i


def linearMap(low, high):
    """
    该函数被autoLevel函数调用，用于计算自动优化过程中的隐射表。
    其本质就是一个带有极化效果的线性映射函数
    :param low: 隐射表下限
    :param high: 隐射表上限
    :return: 某通道的隐射表，根据此表可以计算原颜色在优化后的新图中的色阶值
    """
    mapping = [0] * 256
    for i in range(256):
        if i < low:
            mapping[i] = 0
        elif i > high:
            mapping[i] = 255
        else:
            mapping[i] = np.uint8((i - low) / (high - low) * 255)
    return mapping
