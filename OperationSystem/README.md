# 操作系统

> 经典的408课程，也是本专业的专业必修课，其重要性不言而喻。
>
> 操作系统是一门很有意思的课程，知识大体有结构但细节较多，学习起来较难。
>
> 但操作系统这门课讲授的许多思想可以用于指导代码编写，还是蛮实用的

## 使用环境

* AidLux 1.3.0.477(based on Debian 10)

      实验1~4并不要求特定的Linux发行版，这个就挺小众，也用的好好的。只是后来更新了安卓12，它总是被杀进程，遂弃用。
* Ubuntu 16.04.7 LTS

      仅实验5任务2需要这版系统。
* `gcc`, `vim`
* Visual Studio Code（用于整理代码）
* Microsoft Word（用于写实验报告）

## 教材

* [《计算机操作系统教程》 张尧学，宋虹，张高 编著，清华大学出版社](https://book.douban.com/subject/1928877/)
  * <img alt="计算机操作系统教程" width=256 src="https://img1.doubanio.com/view/subject/s/public/s5790017.jpg">
* [《2022年操作系统考研复习指导》 王道论坛 编著，电子工业出版社](https://book.douban.com/subject/35746559/)
  * <img alt="2022年操作系统考研复习指导" width=256 src="https://bkimg.cdn.bcebos.com/pic/80cb39dbb6fd5266d0164ea4d74b802bd40735fa987a?x-bce-process=image/resize,m_lfit,w_536,limit_1">

## 目录

### [实验PPT](https://pan.quark.cn/s/b8d0433ce89a)

> 跳转到夸克网盘下载

### [实验](./Experiments)

* [实验1：进程管理与进程间通信](./Experiments/Exp1)
  * [源文件](./Experiments/Exp1/Code)
  * 实验报告
    * > 本次实验报告没有上传，反正也挺简单的，就是用gcc编译运行一下几个简单的C程序。

* [实验2：进程调度](./Experiments/Exp2)
  * [源文件](./Experiments/Exp2/Code)
    * 初版：[`source_msvc.c`](./Experiments/Exp2/Code/source_msvc.c)，该文件是我在Windows上使用Visual Studio编译通过的，逻辑没问题，但语法并不契合gcc
    * 修改版：[`source_gcc.c`](./Experiments/Exp2/Code/source_gcc.c)，修改了初版中独属于msvc的语法，该版符合gcc语法，建议直接使用这个
  * 实验报告
    * [Report.pdf](./Experiments/Exp2/Report.pdf)

* [实验3：内存页面置换算法](./Experiments/Exp3)
  * [源文件](./Experiments/Exp3/Code)
    * [`source_gcc.c`](./Experiments/Exp3/Code/source_gcc.c)
  * 实验报告
    * [Report.pdf](./Experiments/Exp3/Report.pdf)

* [实验4：Linux系统状态信息查询](./Experiments/Exp4)
  * [源文件](./Experiments/Exp4/Code)
    * 负载程序: [`load.c`](./Experiments/Exp4/Code/load.c)
    * 脚本1(用于题1)：[`meminfo.sh`](./Experiments/Exp4/Code/meminfo.sh)
    * 脚本2(用于讨论1)：[`meminfo_new.sh`](./Experiments/Exp4/Code/meminfo_new.sh)
    * > 由于我使用的AidLux并非虚拟机，可以使用整台设备的全部内存(8GB)。因此该程序设定的负载较高（10MB/s），以便于观察负载变化。若是使用VMware，请根据自己分配的内存情况手动降低负载调整(通过修改`load.c`，`while`循环中`malloc`和`memset`的值实现)
  * [相关数据](./Experiments/Exp4/Data)
    * 题1数据：[meminfo.sh记录数据](./Experiments/Exp4/Data/1_meminfo.sh记录数据.csv)
    * 题2数据：[vmstat记录数据](./Experiments/Exp4/Data/2_vmstat记录数据.csv)
    * 讨论1数据：[ext_meminfo_new.sh记录数据](./Experiments/Exp4/Data/ext_meminfo_new.sh记录数据.csv)
    * > 这些数据是直接在Terminal上复制得来的，以便于导入Excel进行绘图。当然，不同人得出来的数据是不一样的，这里只是做个参考。
  * 实验报告
    * [Report.pdf](./Experiments/Exp4/Report.pdf)

* [实验5：（期末实验）设备驱动程序](./Experiments/Exp5)
  * [源文件/任务1](./Experiments/Exp5/Exp5_1)
    * 构建脚本：[`Makefile`](./Experiments/Exp5/Exp5_1/Makefile)
    * 字符设备驱动程序：[`chardev.c`](./Experiments/Exp5/Exp5_1/chardev.c)
    * 测试脚本：[`test.c`](./Experiments/Exp5/Exp5_1/test.c)
  * [源文件/任务2](./Experiments/Exp5/Exp5_2)
    * > **注意：** 本部分的代码调用了一些系统库，其中一部分在较新的内核中有改动，使该代码无法正常运行。而我又~~不懂~~不愿意修改该代码，所以选择安装旧版系统。需要使用某些旧版系统如Ubuntu 16。(不清楚内核版本的可以在Terminal中输入`uname -r`查看)
    * 构建脚本：[`Makefile`](./Experiments/Exp5/Exp5_2/Makefile)
    * 块设备驱动程序：[`simp_blkdev.c`](./Experiments/Exp5/Exp5_2/simp_blkdev.c)
    * 代码来源于[2018-2019学年第一学期江苏大学操作系统课程设计教程](https://github.com/LeoB-O/OS-Curriculum-Design)第三题，修改了宏定义中的`SIMP_BLKDEV_BYTES`为50MB，因为原代码的256MB在VMware环境中太大，非常容易在安装模块时触发`Cannot allocate memory`错误。
  * 实验报告
    * [Report.docx](./Experiments/Exp5/Report.docx)
