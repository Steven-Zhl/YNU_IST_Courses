# -*- coding: utf-8 -*
from tkinter import *
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk  # 该库的函数将OpenCV的图转换为TK中图的格式
import ControlPanel
import ProcessImage as Img

__all__ = ['ShowMenu', 'CV2Tk', 'getImagePath', 'setSavePath', 'WindowBase', 'DragCapture', 'MosaicImage', 'GridImage',
           'AttributeImage', 'MosaicImage_Auto', 'AttributeImage_Auto']


# 展示主菜单
def ShowMenu(backImage):
    window = Tk()  # 此为根窗口
    window.configure()
    window.title("图像处理小程序")
    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    width_screen = window.winfo_screenwidth()
    height_screen = window.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (800, 450, (width_screen -
                                800) / 2, (height_screen - 450) / 2)
    window.geometry(alignstr)
    window.resizable(width=False, height=False)  # 设置窗口的长宽均不可变

    # 往窗口上添加按钮
    area_function = Frame(window, width=200)
    Label(window, text="行到水穷处，坐看云起时。", font="楷体",
          fg='black').pack(anchor='ne', padx=5, pady=5)
    Button(area_function, text='创建九宫格图', width=18, command=lambda: ControlPanel.CreateNineGrid()).pack(side='top',
                                                                                                       pady=10)
    Button(area_function, text='拖拽以进行截图', width=18,
           command=lambda: ControlPanel.Capture()).pack(side='top', pady=10)
    Button(area_function, text='指定区域马赛克', width=18, command=lambda: ControlPanel.CreateMosaicImg()).pack(side='top',
                                                                                                         pady=10)
    Button(area_function, text='面部马赛克', width=18, command=lambda: ControlPanel.AutoCreateMosaicImg()).pack(side='top',
                                                                                                           pady=10)
    Button(area_function, text='修改图像参数', width=18, command=lambda: ControlPanel.CreateAttributeImg()).pack(side='top',
                                                                                                           pady=10)
    Button(area_function, text='自适应优化图像', width=18, command=lambda: ControlPanel.AutoAttributeImg()).pack(side='top',
                                                                                                          pady=10)
    Button(area_function, text='退出程序', width=18,
           command=lambda: ControlPanel.Exit()).pack(side='top', pady=10)
    area_function.pack(padx=60, side='left')

    Label(window, width=450, height=450, image=CV2Tk(
        backImage, 450, 450)).pack(anchor='ne')

    window.mainloop()  # 进入消息循环


def CV2Tk(image_CV, width, height):
    global image_convert
    image_convert = cv.resize(
        image_CV, (width, height), interpolation=cv.INTER_AREA)
    image_convert = cv.cvtColor(
        image_convert, cv.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
    image_convert = Image.fromarray(image_convert)  # 将图像转换成Image对象
    image_convert = ImageTk.PhotoImage(
        image=image_convert)  # 将image对象转换为imageTK对象
    return image_convert


# 获取读取的文件路径
def getImagePath():
    path_image = filedialog.askopenfilename(
        title="请选择文件", filetypes=[('图像文件', ['*.jpg', '*.jpeg'])])
    return path_image


# 获取保存文件的目录路径
def setSavePath(title):
    filePath = filedialog.askdirectory(title=title)
    return filePath


class WindowBase:
    def __init__(self, title):
        self.window = Toplevel()
        self.window.title(title)
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (800, 450,
                                    (screenwidth - 800) / 2, (screenheight - 450) / 2)
        self.window.geometry(alignstr)
        self.window.resizable(width=False, height=False)  # 设置窗口的长宽均不可变

    # 为适应画布，需要计算图片应调整至的大小
    @staticmethod
    def calcResize(width_image, height_image, width_canvas, height_canvas):
        if float(width_image / height_image) > float(width_canvas / height_canvas):
            width_resize = width_canvas
            height_resize = int((width_canvas * height_image / width_image))
        else:
            width_resize = int((height_canvas * width_image / height_image))
            height_resize = height_canvas
        return [width_resize, height_resize]

    # 获取读取的文件路径
    @staticmethod
    def getImagePath():
        path_image = filedialog.askopenfilename(
            title="请选择图片", filetypes=[('图像文件', ['*.jpg', '*.jpeg'])])
        return path_image

    # 获取保存文件的目录路径
    @staticmethod
    def setSavePath(title):
        filePath = filedialog.askdirectory(title=title)
        return filePath

    def addLabel(self, master, image_CV):
        height_image = image_CV.shape[0]  # 原图的高度
        width_image = image_CV.shape[1]  # 原图的宽度
        [width_resize, height_resize] = self.calcResize(
            width_image, height_image, 400, 400)
        image_TK = CV2Tk(image_CV, width_resize, height_resize)
        previewImg = Label(master, width=400, height=400, image=image_TK)
        return previewImg


# 拖拽截取图片
class DragCapture(WindowBase):
    def __init__(self):
        super().__init__(title="拖拽以截取图片")
        self.startX = 0
        self.startX = 0
        self.startY = 0
        self.endX = 0
        self.endY = 0
        self.image_temp = None

    def showWindow(self, image_CV):
        # 暂存图，为了能够即时预览与保存
        self.image_temp = image_CV.copy()
        # 添加选项栏
        area_option = Frame(self.window)
        # 添加命名栏
        Label(area_option, text="请为文件命名(不含中文)").pack(side='top', pady=5)
        name = Entry(area_option, width=18)
        name.pack(side='top', pady=5)
        # 添加预览和重设按钮
        Button(area_option, text="预览更改", width=18,
               command=lambda: self.UpdatePreview(self.image_temp, previewImg, 400, 400)).pack(side='top', pady=5)
        Button(area_option, text="重置为原图", width=18,
               command=lambda: self.ResetPreview(image_CV, preview=previewImg, width_pre=400,
                                                 height_pre=400)).pack(side='top', pady=5)
        # 添加保存菜单
        area_save = Frame(area_option)
        Button(area_save, text="保存文件-原画质", width=18,
               command=lambda: Img.save(image_CV=self.image_temp, path_dir=self.setSavePath("保存至"), quality="Origin",
                                        name=name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-高画质", width=18,
               command=lambda: Img.save(image_CV=self.image_temp, path_dir=self.setSavePath("保存至"), quality="High",
                                        name=name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-中画质", width=18,
               command=lambda: Img.save(image_CV=self.image_temp, path_dir=self.setSavePath("保存至"), quality="Medium",
                                        name=name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-低画质", width=18,
               command=lambda: Img.save(image_CV=self.image_temp, path_dir=self.setSavePath("保存至"), quality="Low",
                                        name=name.get())).pack(side='top', pady=5)
        area_save.pack(side='top')
        area_option.pack(side='left', padx=60)

        # 添加动态预览框
        previewImg = self.addLabel(master=self.window, image_CV=image_CV)
        previewImg.bind("<Button-1>", self.OnMouse)
        previewImg.bind("<ButtonRelease-1>", self.ReleaseMouse)
        previewImg.pack(side='right', padx=30)
        self.window.mainloop()

    def OnMouse(self, event):
        self.startX = event.x
        self.startY = event.y
        print(self.startX, self.startY)

    def ReleaseMouse(self, event):
        self.endX = event.x
        self.endY = event.y
        print(self.endX, self.endY)

    def UpdatePreview(self, image_CV, preview, width_pre, height_pre):
        # 确定原本的缩放方式
        if float(image_CV.shape[1] / image_CV.shape[0]) > 1:
            rate = int(image_CV.shape[1] / 400)
        else:
            rate = int(image_CV.shape[0] / 400)
        boundary = [min(self.startX, self.endX), max(self.startX, self.endX), min(self.startY, self.endY),
                    max(self.startY, self.endY)]

        self.image_temp = Img.capturePart(
            image_CV, [i * rate for i in boundary]).copy()
        [width, height] = self.calcResize(
            self.image_temp.shape[1], self.image_temp.shape[0], width_pre, height_pre)
        image_TK = CV2Tk(self.image_temp, width, height)
        preview.configure(image=image_TK)

    def ResetPreview(self, image_CV, preview, width_pre, height_pre):
        self.image_temp = image_CV.copy()
        [width, height] = self.calcResize(
            self.image_temp.shape[1], self.image_temp.shape[0], width_pre, height_pre)
        imgTK = CV2Tk(image_CV, width, height)
        preview.configure(image=imgTK)


# 创建马赛克图
class MosaicImage(WindowBase):
    # 功能-创建马赛克图-更新预览窗口的预览图
    def __init__(self):
        super().__init__(title="图片添加马赛克")
        self.image_temp = None

    def showWindow(self, image_CV):
        self.image_temp = image_CV
        # 向Frame中添加组件
        area_option = Frame(self.window)
        row_x_l = Frame(area_option)
        row_x_r = Frame(area_option)
        row_y_f = Frame(area_option)
        row_y_b = Frame(area_option)
        row_strength = Frame(area_option)
        row_preview = Frame(area_option)
        Label(row_x_l, text="X左边界:", width=8).pack(side='left')
        val_x_l = Entry(row_x_l, width=10)
        val_x_l.pack(side='left')
        Label(row_x_r, text="X右边界:", width=8).pack(side='left')
        val_x_r = Entry(row_x_r, width=10)
        val_x_r.pack(side='left')
        Label(row_y_f, text="Y上边界:", width=8).pack(side='left')
        val_y_f = Entry(row_y_f, width=10)
        val_y_f.pack(side='left')
        Label(row_y_b, text="Y下边界:", width=8).pack(side='left')
        val_y_b = Entry(row_y_b, width=10)
        val_y_b.pack(side='left')
        Label(row_strength, text="马赛克强度(像素数):", width=15).pack(side='left')
        val_strength = Entry(row_strength, width=3)
        val_strength.pack(side='left')
        row_x_l.pack(side='top', pady=5)
        row_x_r.pack(side='top', pady=5)
        row_y_f.pack(side='top', pady=5)
        row_y_b.pack(side='top', pady=5)
        row_strength.pack(side='top', pady=5)
        Label(area_option, text="请为文件命名(不含中文)").pack(side='top', pady=5)
        row_name = Entry(area_option, width=18)
        row_name.pack(side='top', pady=5)

        Button(row_preview, text="预览更改", width=8,
               command=lambda: self.UpdatePreview(image_CV, [int(val_x_l.get()), int(val_x_r.get()), int(val_y_f.get()),
                                                             int(val_y_b.get())], int(val_strength.get()),
                                                  preview)).pack(side='left', pady=5)
        Button(row_preview, text="重置", width=8,
               command=lambda: self.UpdatePreview(image_CV, None, 0, preview)).pack(side='left', pady=5)
        row_preview.pack(side='top', pady=5)
        area_save = Frame(area_option)
        Button(area_save, text="保存文件-原画质", width=18,
               command=lambda: Img.save(image_CV=self.image_temp, path_dir=self.setSavePath("保存至"), quality="Origin",
                                        name=row_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-高画质", width=18,
               command=lambda: Img.save(image_CV=self.image_temp, path_dir=self.setSavePath("保存至"), quality="High",
                                        name=row_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-中画质", width=18,
               command=lambda: Img.save(image_CV=self.image_temp, path_dir=self.setSavePath("保存至"), quality="Medium",
                                        name=row_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-低画质", width=18,
               command=lambda: Img.save(image_CV=self.image_temp, path_dir=self.setSavePath("保存至"), quality="Low",
                                        name=row_name.get())).pack(side='top', pady=5)
        area_save.pack(side='top')
        area_option.pack(side='left', padx=60)
        # 设置画布参数
        preview = self.addLabel(self.window, image_CV)
        preview.pack(side='right', padx=30)
        self.window.mainloop()

    def UpdatePreview(self, image_CV, boundary, mosaicStrength, preview):
        if boundary is not None:  # boundary is None说明是更新原图而非展示预览图
            self.image_temp = Img.addMosaic(
                image_CV=image_CV, boundary=boundary, strength=mosaicStrength)
        else:
            self.image_temp = image_CV.copy()
        width_resize, height_resize = self.calcResize(
            image_CV.shape[1], image_CV.shape[0], 400, 400)
        image_TK = CV2Tk(self.image_temp, width_resize, height_resize)
        preview.configure(image=image_TK)


# 创建九宫格图
class GridImage(WindowBase):
    def __init__(self):
        super().__init__(title="生成九宫格图")
        self.image_CV_List = []
        self.tkList = []

    def showWindow(self, imgCV_List):
        for i in imgCV_List:
            self.image_CV_List.append(i.copy())

        # 添加Frame组件
        area_option = Frame(self.window)
        Label(area_option, text="请为文件命名(不含中文)").pack(side='top', pady=5)
        area_name = Entry(area_option, width=18)
        area_save = Frame(area_option)
        Button(area_save, text="保存文件-原画质", width=18,
               command=lambda: Img.save(image_CV=self.image_CV_List, path_dir=self.setSavePath("保存至"), quality="Origin",
                                        name=area_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-高画质", width=18,
               command=lambda: Img.save(image_CV=self.image_CV_List, path_dir=self.setSavePath("保存至"), quality="High",
                                        name=area_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-中画质", width=18,
               command=lambda: Img.save(image_CV=self.image_CV_List, path_dir=self.setSavePath("保存至"), quality="Medium",
                                        name=area_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-低画质", width=18,
               command=lambda: Img.save(image_CV=self.image_CV_List, path_dir=self.setSavePath("保存至"), quality="Low",
                                        name=area_name.get())).pack(side='top', pady=5)
        area_name.pack(side='top', pady=5)
        area_save.pack(side='top', pady=5)
        area_option.pack(side='left', padx=60)

        # 计算缩放宽度和高度
        [reWidth, reHeight] = self.calcResize(
            imgCV_List[0].shape[1], imgCV_List[0].shape[0], 400 // 3, 400 // 3)
        self.tkList = [CV2Tk(i, reWidth, reHeight) for i in self.image_CV_List]
        # 计算绘图所需的的锚点以及其他变量
        edge = 5  # 设定边框为5像素（在绘图区中）
        topEdge = int((400 - (3 * reHeight) - 4 * edge) / 2)  # 上边界宽度

        # 创建画布
        preview = Canvas(self.window, width=400, height=400)
        preview.pack(side='right', padx=30)
        # 绘图
        for row in range(0, 3):
            for col in range(0, 3):
                preview.create_image((col + 1) * edge + col * reWidth, topEdge + (row + 1) * edge + row * reHeight,
                                     image=self.tkList[col + 3 * row], anchor='nw')
        self.window.mainloop()


# 调整图像参数
class AttributeImage(WindowBase):
    def __init__(self):
        super().__init__(title="图像参数调整")
        self.tempImg = None

    def showWindow(self, image_CV):
        self.tempImg = image_CV
        # 添加参数标签栏
        area_attribute = Frame(self.window)
        area_label = Frame(area_attribute)
        Label(area_label, text='亮度', width=4).pack(side='left')
        Label(area_label, text='色度', width=5).pack(side='left')
        Label(area_label, text='对比度', width=5).pack(side='left')
        Label(area_label, text='锐度', width=4).pack(side='left')
        area_label.pack(side='top')
        # 添加参数滑块区域
        area_scale = Frame(area_attribute)
        val_brightness = Scale(area_scale, from_=2, to=-1,
                               resolution=0.1, width=4, length=150)
        val_brightness.pack(side='left')
        val_color = Scale(area_scale, from_=2, to=-1,
                          resolution=0.1, width=5, length=150)
        val_color.pack(side='left')
        val_contrast = Scale(area_scale, from_=2, to=-1,
                             resolution=0.1, width=4, length=150)
        val_contrast.pack(side='left')
        val_sharpness = Scale(area_scale, from_=2, to=-1,
                              resolution=0.1, width=5, length=150)
        val_sharpness.pack(side='left')
        area_scale.pack(side='top')
        # 添加功能区域
        Label(area_attribute, text="请为文件命名(不含中文)").pack(side='top', pady=5)
        area_name = Entry(area_attribute, width=18)
        area_name.pack(side='top', pady=5)
        Button(area_attribute, text="效果预览", width=18,
               command=lambda: self.UpdatePreview(image_CV, [float(val_brightness.get()), float(val_color.get()),
                                                             float(val_contrast.get()), float(val_sharpness.get())],
                                                  resizeWidth, resizeHeight, preview)).pack(side='top')
        area_save = Frame(area_attribute)
        Button(area_save, text="保存文件-原画质", width=18,
               command=lambda: Img.save(image_CV=self.tempImg, path_dir=self.setSavePath("保存至"), quality="Origin",
                                        name=area_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-高画质", width=18,
               command=lambda: Img.save(image_CV=self.tempImg, path_dir=self.setSavePath("保存至"), quality="High",
                                        name=area_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-中画质", width=18,
               command=lambda: Img.save(image_CV=self.tempImg, path_dir=self.setSavePath("保存至"), quality="Medium",
                                        name=area_name.get())).pack(side='top', pady=5)
        Button(area_save, text="保存文件-低画质", width=18,
               command=lambda: Img.save(image_CV=self.tempImg, path_dir=self.setSavePath("保存至"), quality="Low",
                                        name=area_name.get())).pack(side='top', pady=5)
        area_save.pack(side='top', pady=5)
        area_attribute.pack(side='left', padx=60)
        # 添加画布
        [resizeWidth, resizeHeight] = self.calcResize(
            image_CV.shape[1], image_CV.shape[0], 400, 400)
        preview = self.addLabel(self.window, image_CV=image_CV)
        preview.pack(side='right', padx=30)
        self.window.mainloop()

    # 功能-调整图像参数-更新预览窗口的预览图
    def UpdatePreview(self, image_CV, strength, width, height, preview):
        newPic = Img.enhance(image_CV, strength)
        self.tempImg = newPic.copy()
        image_TK = CV2Tk(self.tempImg, width, height)
        preview.configure(image=image_TK)


# 自动创建马赛克图
class MosaicImage_Auto(WindowBase):
    def __init__(self, axis):
        super().__init__("定位人脸并添加马赛克")
        self.tempMosaicImg = None
        self.facesLocation = axis

    def showWindow(self, image_CV):
        self.tempMosaicImg = image_CV.copy()
        # 向Frame中添加组件
        attribute = Frame(self.window)
        Label(attribute, text="马赛克强度(色块边长):").pack(side='top')
        MosaicStrengthVal = Entry(attribute)
        MosaicStrengthVal.pack(side='top')
        Label(attribute, text="请为文件命名(不含中文):").pack(side='top')
        NameVal = Entry(attribute)
        NameVal.pack(side='top')
        # 添加按钮组件
        Button(attribute, text="显示预览效果", width=18,
               command=lambda: self.UpdatePreview(image_CV=image_CV, axis=self.facesLocation,
                                                  mosaicStrength=int(MosaicStrengthVal.get()), width=width_resize,
                                                  height=height_resize, preview=previewImg)).pack(side='top',
                                                                                                  pady=5)
        Button(attribute, text="显示原图", width=18,
               command=lambda: self.ResetPreview(image_CV, previewImg, 400, 400)).pack(side='top', pady=5)
        Button(attribute, text="保存文件-原画质", width=18,
               command=lambda: Img.save(image_CV=self.tempMosaicImg, path_dir=self.setSavePath("另存为"), quality="Origin",
                                        name=NameVal.get())).pack(side='top', pady=5)
        Button(attribute, text="保存文件-高画质", width=18,
               command=lambda: Img.save(image_CV=self.tempMosaicImg, path_dir=self.setSavePath("另存为"), quality="High",
                                        name=NameVal.get())).pack(side='top', pady=5)
        Button(attribute, text="保存文件-中画质", width=18,
               command=lambda: Img.save(image_CV=self.tempMosaicImg, path_dir=self.setSavePath("另存为"), quality="Medium",
                                        name=NameVal.get())).pack(side='top', pady=5)
        Button(attribute, text="保存文件-低画质", width=18,
               command=lambda: Img.save(image_CV=self.tempMosaicImg, path_dir=self.setSavePath("另存为"), quality="Low",
                                        name=NameVal.get())).pack(side='top', pady=5)
        attribute.pack(side=LEFT, padx=60)
        # 设置画布参数
        [width_resize, height_resize] = self.calcResize(
            image_CV.shape[1], image_CV.shape[0], 400, 400)
        image_TK = CV2Tk(image_CV, width_resize, height_resize)
        previewImg = Label(self.window, width=400, height=400, image=image_TK)
        previewImg.pack(side='right', padx=30)
        self.window.mainloop()

    def UpdatePreview(self, image_CV, axis, mosaicStrength, width, height, preview):
        mosaicPic = Img.addMosaic(image_CV=image_CV, boundary=[(axis[0])[0], (axis[0])[0] + (axis[0])[2], (axis[0])[1],
                                                               (axis[0])[1] + (axis[0])[3]], strength=mosaicStrength)
        self.tempMosaicImg = mosaicPic.copy()
        imgWithTK = CV2Tk(mosaicPic, width, height)
        preview.configure(image=imgWithTK)

    def ResetPreview(self, image_CV, preview, previewWidth, previewHeight):
        self.tempMosaicImg = image_CV
        [width, height] = self.calcResize(
            image_CV.shape[1], image_CV.shape[0], previewWidth, previewHeight)
        imgTK = CV2Tk(image_CV, width, height)
        preview.configure(image=imgTK)


# 自动优化参数
class AttributeImage_Auto(WindowBase):
    def __init__(self):
        super().__init__(title="自动优化参数")
        self.tempImg = None

    def showWindow(self, image_CV):
        self.tempImg = image_CV

        # 添加参数标签栏
        area_function = Frame(self.window)
        Label(area_function, text="请为图片命名:").pack(side='top', pady=5)
        NameVal = Entry(area_function)
        NameVal.pack(side='top', pady=5)
        Button(area_function, text="效果预览", width=18,
               command=lambda: self.UpdatePreview(image_CV, 400, 400, preview)).pack(side='top', pady=5)
        Button(area_function, text="显示原图", width=18,
               command=lambda: self.ResetPreview(image_CV, 400, 400, preview)).pack(side='top', pady=5)
        Button(area_function, text="保存文件-原画质", width=18,
               command=lambda: Img.save(self.tempImg, self.setSavePath("另存为"), quality="Origin",
                                        name=NameVal.get())).pack(side='top', pady=5)
        Button(area_function, text="保存文件-高画质", width=18,
               command=lambda: Img.save(self.tempImg, self.setSavePath("另存为"), quality="High",
                                        name=NameVal.get())).pack(side='top', pady=5)
        Button(area_function, text="保存文件-中画质", width=18,
               command=lambda: Img.save(self.tempImg, self.setSavePath("另存为"), quality="Medium",
                                        name=NameVal.get())).pack(side='top', pady=5)
        Button(area_function, text="保存文件-低画质", width=18,
               command=lambda: Img.save(self.tempImg, self.setSavePath("另存为"), quality="Low",
                                        name=NameVal.get())).pack(side='top', pady=5)
        area_function.pack(side='left', padx=60)

        # 添加画布
        [resizeWidth, resizeHeight] = self.calcResize(
            image_CV.shape[1], image_CV.shape[0], 400, 400)
        image_TK = CV2Tk(image_CV, resizeWidth, resizeHeight)
        preview = Label(self.window, width=400, height=400, image=image_TK)
        preview.pack(side='right', padx=30)

        self.window.mainloop()

    # 功能-调整图像参数-更新预览窗口的预览图
    def UpdatePreview(self, image_CV, width, height, preview):
        newPic = Img.autoEnhance(image_CV)
        self.tempImg = newPic
        [resizeWidth, resizeHeight] = self.calcResize(
            image_CV.shape[1], image_CV.shape[0], width, height)
        imgTK = CV2Tk(self.tempImg, resizeWidth, resizeHeight)
        preview.configure(image=imgTK)

    def ResetPreview(self, image_CV, width, height, preview):
        self.tempImg = image_CV
        [resizeWidth, resizeHeight] = self.calcResize(
            image_CV.shape[1], image_CV.shape[0], width, height)
        imgTK = CV2Tk(self.tempImg, resizeWidth, resizeHeight)
        preview.configure(image=imgTK)
