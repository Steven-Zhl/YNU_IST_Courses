# 《计算机网络》课程的相关资料

> 经典的408课程，也是本专业的专业必修课，其重要性不言而喻。
>
> 但是相比于其他三门408专业课，计算机网络的内容是最贴近实际的，其中讲的很多算法、协议直至现在还在广泛使用，所以也是最有意思的，其实用性比其他三门高很多。

## 使用环境

* Windows 11
* Packet Tracer 8.2.0
* Microsoft Word（用于写实验报告）

## 教材

* [《计算机网络（第八版）》 谢希仁 编著，电子工业出版社](https://book.douban.com/subject/35498120/)
  * <img alt="计算机网络（第八版）" width=256 src="https://img1.doubanio.com/view/subject/s/public/s33983450.jpg">
* [《计算机网络实验指导书》 郭雅，李泗兰 主编，电子工业出版社](https://book.douban.com/subject/30822318/)：记得买新版的，旧版书里有些指令已经在新版的Packet Tracer中被删掉了
  * <img alt="计算机网络实验指导书" width=256 src="https://bkimg.cdn.bcebos.com/pic/3c6d55fbb2fb43166d22514020f6512309f7905275f5?x-bce-process=image/resize,m_lfit,w_536,limit_1">
* [《2022年计算机网络考研复习指导》 王道论坛 组编，电子工业出版社](https://book.douban.com/subject/35312985/)

## 目录

### 课程

* 跳转到[津宝的Repository](https://github.com/wangjin0818/Computer_Network_2023/)中查看

### [作业](./Homework)

* 雨课堂作业(做的不太好QAQ)
  * [作业1](./Homework/Hwk1.mhtml)
  * [作业2](./Homework/Hwk2.mhtml)
  * [作业3](./Homework/Hwk3.mhtml)
  * [作业4](./Homework/Hwk4.mhtml)

### [实验](./Experiments)

* [Packet Tracer汉化包](./Experiments/Chinese_chi.ptl)
  * 亲测可在Packet Tracer 8.2.0（Windows版）上稳定运行。
  * 使用方法：下载后将其移动至`~/languages`路径下。然后打开软件，依次点击`Options-Preferences-Interface`，在下方`Select Language`中选择"Chinese_chi.ptl"，然后点击右侧`Change Language`，随后重启即可生效。
  * 感谢汉化包作者[湖科大教书匠](https://space.bilibili.com/360996402)老师。此外，老师的Packet Tracer仿真实验系列视频也非常不错，适合系统学习、练习计算机网络。

* 实验3: 子网掩码与划分子网
  * 源文件：[`exp3.pkt`](./Experiments/Exp3/exp3.pkt)
  * 实验报告：[Report.pdf](./Experiments/Exp3/Report.pdf)

* 实验4: 交换机基本配置
  * 源文件：[`exp4.pkt`](./Experiments/Exp4/exp4.pkt)
  * 实验报告：[Report.pdf](./Experiments/Exp4/Report.pdf)

* 实验5: 管理MAC地址转发表
  * 源文件：[`exp5.pkt`](./Experiments/Exp5/exp5.pkt)
  * 实验报告：[Report.pdf](./Experiments/Exp5/Report.pdf)

* 实验6: 虚拟局域网（VLAN）实验
  * 源文件：[`exp6.pkt`](./Experiments/Exp6/exp6.pkt)
  * 实验报告：[Report.pdf](./Experiments/Exp6/Report.pdf)

* 实验7: 三层交换机的配置
  * 源文件：[`exp7.pkt`](./Experiments/Exp7/exp7.pkt)
  * 实验报告：[Report7-9.pdf](./Experiments/Report7-9.pdf)

* 实验8: 三层交换机的访问控制
  * 源文件：[`exp8.pkt`](./Experiments/Exp8/exp8.pkt)
  * 实验报告：[Report7-9.pdf](./Experiments/Report7-9.pdf)

* 实验9: 三层交换机的综合实验
  * 源文件：[`exp9.pkt`](./Experiments/Exp9/exp9.pkt)
  * 实验报告：[Report7-9.pdf](./Experiments/Report7-9.pdf)

* 实验10: 路由器的基本配置
  * 源文件：[`exp10.pkt`](./Experiments/Exp10/exp10.pkt)
  * 实验报告：[Report10-12.pdf](./Experiments/Report10-12.pdf)

* 实验11: 静态路由实验
  * 源文件：[`exp11.pkt`](./Experiments/Exp11/exp11.pkt)
  * 实验报告：[Report10-12.pdf](./Experiments/Report10-12.pdf)

* 实验12: 路由信息协议(RIP)实验
  * 源文件：[`exp12.pkt`](./Experiments/Exp12/exp12.pkt)
  * 实验报告：[Report12-14.pdf](./Experiments/Report12-14.pdf)

* 实验13: 开放最短路径优先(OSPF)实验
  * 源文件：[`exp13.pkt`](./Experiments/Exp13/exp13.pkt)
  * 实验报告：[Report12-14.pdf](./Experiments/Report12-14.pdf)

* 实验14: 访问控制列表(ACL)实验
  * 源文件：[`exp14.pkt`](./Experiments/Exp14/exp14.pkt)
  * 实验报告：[Report12-14.pdf](./Experiments/Report12-14.pdf)

* 实验15: 《计算机网络实验》期末综合设计
  * 设计要求：[计算机网络实验-期末考核要求.pdf](./Experiments/Exp15-期末实验_校园网搭建/计算机网络实验-期末考核要求.pdf)
  * VLAN设计：[VLAN_Design.drawio](./Experiments/Exp15-期末实验_校园网搭建/VLAN_Design.drawio)
  * 说明文档：[README.md](./Experiments/Exp15-期末实验_校园网搭建/README.md)，鉴于本次实验项目比较复杂，特编辑了一份说明文档，以便于大家理解
  * 源文件：[exp15.pkt](./Experiments/Exp15-期末实验_校园网搭建/exp15.pkt)
  * 实验报告：[Report.pdf](./Experiments/Exp15-期末实验_校园网搭建/Report.pdf)
