# 《毕业设计》

> 存放毕业设计的相关资料，论文写的很水，就不放出来了，仅提供一些参考资料和个人建议。

* 我做的毕设是交通流量预测方向的，属于时序预测的范畴，骨干网络(Backbone)是Transformer，具体实现基于PyTorch。

## 使用环境

### 服务器配置

* Intel Xeon Platinum 8352V
* NVIDIA GeForce RTX 4090 24GB
* Ubuntu 22.04.3 LTS
* Python 3.10.8
  * PyTorch 2.1.2+cu121

### PC配置

* Windows 11 Pro 23H2
* [TeX Live 2024](https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/)

## 个人建议

* 论文撰写工具：写论文时LaTeX和Word是最主要的两种选择，虽然学校提供的写作模板、格式要求都是基于Word的，但我更推荐使用LaTeX。LaTeX在参考文献管理、版式控制、定制化程度上都更高，况且现在还有一份学长制作的[LaTeX模板](https://github.com/Astro-Lee/YNU-thesis-bachelor)，使用起来已经很方便了。唯一不便的可能就是公式和表格的撰写，但是....现在写论文一般都会用点GPT的吧，这种工作交给AI就好了。
* 论文插图：首先最重要的一点是，配图一定要足够清晰！
  * 绘图工具：
    * 首推draw.io，[开源](https://github.com/jgraph/drawio-desktop)、轻量、导出格式多、元素丰富，并且默认配色(软件右侧“样式”中的一些颜色)就已经足够好看(《Attention is All You Need》的[传世经典图](https://arxiv.org/html/1706.03762v7/extracted/1706.03762v7/Figures/ModalNet-21.png)同款配色)，稍微调一调线宽就能画出很有高级感的图。
    * 其次推荐Visio，同样称得上功能强大，但相比于draw.io就逊色不少了：源文件是私有格式、导出格式少、软件体积大，以及最重要的：收费。
    * 根据“智能科学与技术”的实际情况来看，最常用的编程语言是Python，其次是MATLAB。Python中毫无疑问地推荐matplotlib，而MATLAB使用自带的绘图功能就完全足够了。
    * 除了以上几个直接绘图的方式，还有一些间接绘图的方式，比如TensorBoard，但由于这种方式不太常用，就不再多说了。
  * 文件格式：首先是毫无疑问的，矢量图 > 位图
    * 矢量图比较推荐的格式是pdf和eps。pdf格式的图片在Word和LaTeX的兼容性都很好，比较推荐。Word已不支持eps格式了，但LaTeX中目前仍能较好地兼容，因此仅当使用LaTeX时推荐使用eps格式，而且导出eps文件会比pdf要小。而svg是不推荐的，因为在Word中元素位置有可能会出现偏差，而LaTeX对其兼容性不好。
    * 位图就是常见的png和jp(e)g了，只要足够清晰也是不错的，值得说道的不多。由于png可以存储透明像素而jpeg不行，所以通常来说推荐使用png格式。
* 引文格式：通常来说，论文的引文格式都要求采用GB/T 7714-2015标准。
  * 如果是在Word中写作，只要复制论文网站中这一类型的参考文献内容即可。
  * 在LaTeX中，需要使用bibtex格式的引文内容，大多数论文网站也支持导出该格式的引文，只需要将其复制到.bib文件中即可。
* 论文学习：
  * 计算机相关领域，较新较好的论文都是英文的(嗯，事实就是如此)，但是在看论文时，本身英文就是个障碍，再加上论文中的专业术语，很多时候会让人望而生畏。
  * 这时候你可以试试以下几个途径中有无相关的文献解读：知乎、博客园、CSDN、微信公众号、B站。
  * 如果都没有的话，再去试试翻译一下原文。这里不推荐直接翻译pdf，而是使用各网站提供的在线预览功能，结合[沉浸式翻译](https://immersivetranslate.com/)插件，这样可以最大程度保留原文的格式，也能更好地理解原文的内容。

## 一些自己的经验总结

* [[毕设版]draw.io的使用方法](./[毕设版]draw.io的使用方法.md)

## 参考资料

* LaTeX
  * [Overleaf](https://www.overleaf.com/) : 在线LaTeX编辑器，云大本科生论文模板也有！
  * [Overleaf](https://cn.overleaf.com/) : Overleaf国内版
  * [LaTeX模板](https://github.com/Astro-Lee/YNU-thesis-bachelor) : 非常不错的本科生毕业设计LaTeX模板，亲测可用于毕业设计，效果很好。
* 论文资源
  * [中国知网](http://www.cnki.net/) : “XXX：‘知网是什么东西？’”
  * [Google Scholar](https://scholar.google.com/) : 永远的神！
  * [arXiv](https://arxiv.org/) : 一个著名的预印本网站，很多计算机方面的优秀论文都会率先在这里发表。
  * [Papers With Code](https://paperswithcode.com/) : 宝藏网站，可以根据研究方向查找相关论文，很多论文还都附带了开源代码。
  * [IEEE Xplore](https://ieeexplore.ieee.org/) : IEEE的论文数据库，质量很高。
* 绘图工具
  * [draw.io](https://app.diagrams.net/) : 开源、轻量、导出格式多、元素丰富。
  * [Visio](https://www.microsoft.com/zh-cn/microsoft-365/visio/flowchart-software) : 功能强大，但收费。
  * [matplotlib](https://matplotlib.org/) : Python中最常用的绘图库。
* 算力：租用服务器
  * [AutoDL(算力云)](https://www.autodl.com/) : 按量计费是好文明，硬件配置也很不错，并且在算力云上创建实例时可以直接配好相关环境(PyTorch、Tensorflow等)，服务很好。
  * SSH : ssh是一种远程连接协议，我个人非常喜欢使用VS Code通过ssh连接服务器，大多数云服务器也支持ssh连接。
