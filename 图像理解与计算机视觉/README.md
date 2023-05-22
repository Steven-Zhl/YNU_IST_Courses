# 图像理解与计算机视觉

> 这是一门注重实践的课，虽然会学习很多相关算法，但都是图像处理领域的经典算法，没那么难理解。相比之下，将其用代码实现显得更有意义。
>
> 本课程并不涉及机器学习和深度学习，但其中所学的方法却常被用于机器学习的预处理和后处理中。因此，本课程对于计算机视觉领域的机器学习有较高的实用价值。
>
> 但实话讲，这门课也是我最失望的一门，希望越大失望越大，本来我以为这门课会非常实用，且有成就感，但老师太过照本宣科，灵活和创新不足，使得我渐渐丧失了这门课的热情。
>
> 这门课平时实验、作业、思政报告都不少，但期末考试放大水拉了一波好感。尽管如此，我还是不太喜欢这位老师。

## 使用环境

* Windows 11
* Matlab R2022a
* Visual Studio Code
* Microsoft Word（用于写实验报告）
* Draw.io（用于绘图）

## 教材

> 本课程并无指定教材，以下两本书均为参考书目

* [《数字图像处理（第四版）》，Rafael C. Gonzalez 等著，阮秋琦 等译，电子工业出版社，2020.05](https://book.douban.com/subject/35075811/)
  * 就是著名的冈萨雷斯的“那本厚书”
  * <img alt="数字图像处理（第四版）" width=256 src="https://img1.doubanio.com/view/subject/s/public/s33689157.jpg">
* [《数字图像处理》贾永红 著，武汉大学出版社，2015.07](https://book.douban.com/subject/4712057/)
  * <img alt="数字图像处理" src="https://img2.doubanio.com/view/subject/s/public/s6143481.jpg">

## 目录

### [课程](https://www.aliyundrive.com/s/WA1eNP9V7dp)

> 去阿里云盘下载PPT

* 有一说一，虽然我不喜欢她的教课风格，但PPT做的确实非常认真。

### 实验

* [实验1：图像变换](./Experiments/Exp1/)
  * 项目：[Code](./Experiments/Exp1/Code)
    * 主程序：[`Exp1.m`](./Experiments/Exp1/Code/Exp1.m)
  * 实验报告：[Report.pdf](./Experiments/Exp1/Report.pdf)
  * References
    * `equalizeImg(img, bin)` (灰度直方图均衡化)
      * [图像数据的直方图 - MATLAB imhist - MathWorks 中国](https://ww2.mathworks.cn/help/images/ref/imhist.html?s_tid=doc_ta#buo3qek-1-binLocations)

* [实验2：图像滤波](./Experiments/Exp2/)
  * 项目：[Code](./Experiments/Exp2/Code)
    * 主程序：[`Exp2.m`](./Experiments/Exp2/Code/Exp2.m)
  * 实验报告：[Report.pdf](./Experiments/Exp2/Report.pdf)
  * References
    * `freq_laplace_filter()` (频域拉普拉斯滤波)
      * [灰度图像的频率域滤波——拉普拉斯——高频提升（Matlab）_lengo的博客-CSDN博客](https://blog.csdn.net/lengo/article/details/100527930)
    * (理解图像频域及频域滤波)
      * [什么是图像上的频率？_Norstc的博客-CSDN博客_图像空间频率](https://blog.csdn.net/a493823882/article/details/117925648)
      * [如何理解图像的频率域处理？ - 知乎](https://zhuanlan.zhihu.com/p/484475975)

* [实验3：图像复原](./Experiments/Exp3/)
  * 项目：[Code](./Experiments/Exp3/Code)
    * 主程序：[`Exp3.m`](./Experiments/Exp3/Code/Exp3.m)
  * 实验报告：[Report.pdf](./Experiments/Exp3/Report.pdf)
  * References：(无)

* [实验4：形态学处理](./Experiments/Exp4/)
  * 项目：[Code](./Experiments/Exp4/Code)
    * 主程序：[`Exp4.m`](./Experiments/Exp4/Code/Exp4.m)
  * 实验报告：[Report.pdf](./Experiments/Exp4/Report.pdf)
  * References：(无)

* [实验5：图像分割](./Experiments/Exp5/)
  * 项目：[Code](./Experiments/Exp5/Code)
    * 主程序：[`Exp5.m`](./Experiments/Exp5/Code/Exp5.m)
  * 实验报告：[Report.pdf](./Experiments/Exp5/Report.pdf)
  * References：有很多，但因为当时的搜索记录并未及时保留，暂无法列出。

* [实验6：图像描述](./Experiments/Exp6/)
  * 项目：[Code](./Experiments/Exp6/Code)
    * 主程序：[`Exp6.m`](./Experiments/Exp6/Code/Exp6.m)
  * > 对于`sift`算法，需要下载`siftWin32.exe`文件，并将其放在Matlab安装路径的`bin`文件夹下才可使用。不提供具体下载链接了，自行搜索即可。
  * 实验报告：[Report.pdf](./Experiments/Exp6/Report.pdf)
  * References
    * (SIFT算法)
      * [SIFT(2)——MATLAB实现SIFT详解_海淀摆烂王的博客-CSDN博客_matlab sift](https://blog.csdn.net/qq_20778015/article/details/83188551)
      * [(原作者博客)Keypoint dectetor](https://www.cs.ubc.ca/~lowe/keypoints/)
    * `Canny_edge_detect(img_gray)` (Canny算子边缘检测)
      * [Canny边缘检测算法 - 知乎](https://zhuanlan.zhihu.com/p/99959996)
    * `HOG(img_gray)` (HOG特征算法)
      * [【特征检测】HOG特征算法_hujingshuang的博客-CSDN博客_hog特征检测](https://blog.csdn.net/hujingshuang/article/details/47337707)

* [实验7：计算机视觉典型应用](./Experiments/Exp7/)
  * 项目：[Code](./Experiments/Exp7/Code)
    * 主程序：[`Exp7.m`](./Experiments/Exp7/Code/Exp7.m)
    * > 该程序不包含测试视频`pedestrian.avi`，请自行下载后移动至`./Experiments/Exp7/Code`文件夹下。
      >
      > 该程序中不包含测试数据集`Girl2`，请自行下载解压后移动至`./Experiments/Exp7/Code/tracker/`文件夹下。
      >
      > 这两份文件老师应当会提供的
    * 实验报告：[Report.pdf](./Experiments/Exp7/Report.pdf)
    * References
      * `frame_difference_3(video, frame_num)` (三帧差分法)
        * [初学者做三帧差分（matlab代码）_qq_45087091的博客-CSDN博客](https://blog.csdn.net/qq_45087091/article/details/94625040)
      * `gauss_bg_modeling(video)` (混合高斯背景建模)
        * [matlab 混合高斯背景建模的实现_大米粥哥哥的博客-CSDN博客_高斯混合模型背景建模matlab](https://blog.csdn.net/qq_38204686/article/details/104508018)
      * (KCF 运动目标追踪)
        * [(原理讲解)KCF跟踪算法原理 入门详解 - Jerry_Jin - 博客园](https://www.cnblogs.com/jins-note/p/10215511.html)
        * [(代码调试)KCF代码调试并显示效果（matlab）_無負今日的博客-CSDN博客_kcf算法matlab代码](https://blog.csdn.net/weixin_44100850/article/details/102840630)
        * [(原版代码)João F. Henriques](https://www.robots.ox.ac.uk/~joao/downloads/tracker_release2.zip)
        * [(原论文)Your Title](https://www.robots.ox.ac.uk/~joao/publications/henriques_tpami2015.pdf)
      * [(相关测试集下载)Visual Tracker Benchmark](http://cvlab.hanyang.ac.kr/tracker_benchmark/datasets.html)

### [作业](./Homework)

* [作业1：图像变换](./Homework/Hwk1)
  * 计算表格：[最后一题计算表格.xlsx](./Homework/Hwk1/最后一题计算表格.xlsx)
  * 报告：[作业1.md](./Homework/Hwk1/作业1.md)

* [作业2：图像增强](./Homework/Hwk2)
  * 题目：[CH02-课后作业.pdf](./Homework/Hwk2/CH02-课后作业.pdf)
  * 报告：[作业2.md](./Homework/Hwk2/作业2.md)

* [作业3：图像复原](./Homework/Hwk3)
  * 题目：[CH03-课后作业.pdf](./Homework/Hwk3/CH03-课后作业.pdf)
  * 报告：[作业3.md](./Homework/Hwk3/作业3.md)

* [作业4：图像压缩](./Homework/Hwk4)
  * 题目：[CH04-课后作业.pdf](./Homework/Hwk4/CH04-课后作业.pdf)
  * 报告：[作业4.md](./Homework/Hwk4/作业4.md)

* [作业5：形态学处理](./Homework/Hwk5)
  * 题目：[CH05-课后作业.pdf](./Homework/Hwk5/CH05-课后作业.pdf)
  * 报告：[作业5.md](./Homework/Hwk5/作业5.md)

* [作业6：图像分割](./Homework/Hwk6)
  * 题目：[CH06-课后作业.pdf](./Homework/Hwk6/CH06-课后作业.pdf)
  * 报告：[作业6.md](./Homework/Hwk6/作业6.md)

* [作业7：图像描述](./Homework/Hwk7)
  * 题目：[CH07-课后作业.pdf](./Homework/Hwk7/CH07-课后作业.pdf)
  * 报告：[作业7.md](./Homework/Hwk7/作业7.md)

* [作业8：计算机视觉典型应用](./Homework/Hwk8)
  * 题目：[CH08-课后作业.pdf](./Homework/Hwk8/CH08-课后作业.pdf)
  * 报告：[作业8.md](./Homework/Hwk8/作业8.md)

* [作业9：计算机视觉前沿技术](./Homework/Hwk9)
  * 题目：[CH09-课后作业.pdf](./Homework/Hwk9/CH09-课后作业.pdf)
  * 报告：[作业9.md](./Homework/Hwk9/作业9.md)

* 部分绘图源文件：[作业绘图.drawio](./Homework/作业绘图.drawio)
