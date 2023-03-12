# 机器人学导论

> 这是一门更注重于工程和硬件的课程，这门课的主题内容都是解决实际控制中的需求和问题的。
>
> 包括如何操作舵机与伺服电机，PID控制体系，如何编程实现遥控等等，虽然很基础，但确实很有意思。
>
> 此外，这门课给分很不错。

## 使用环境

* Windows 10
* Keil µVision 5（主要的IDE）
* mcuisp(for stm32)（用于串口通信与项目烧录）
* > 这两份软件老师会提供的。
* Visual Studio Code（C/C++ environment）
* Matlab R2022a（用于PID控制的仿真测试）

## 教材

* [《机器人系统设计及其应用技术》，赵建伟 主编，清华大学出版社](https://book.douban.com/subject/27190685/)
  * <img alt="机器人系统设计及其应用技术" width=256 src="https://bkimg.cdn.bcebos.com/pic/b219ebc4b74543a98226771833479d82b9014b90be9d?x-bce-process=image/resize,m_lfit,w_536,limit_1">

## 特别感谢

    独木不林，单弦不音，这是1组成员共同的成果。感谢捷哥、帆哥、铓哥、龙哥、喆哥的共同努力。

## 目录

* 实验1：配置开发环境
  * > 即安装Keil µVision 5、mcuisp等软件，内容略

* [实验2：编程控制1](./Experiments/Exp2：编程控制1)
  * 源文件：[CAR_STM32F103C6.7z](https://pan.quark.cn/s/106f296f21af)
  * 实验报告：[Report.docx](https://pan.quark.cn/s/106f296f21af)
  * 实验要求：[实验要求.docx](./Experiments/Exp2：编程控制1/实验要求.docx)

* 实验3：编程控制2
  * > 咕咕咕....
  * 源文件
  * 实验报告
  * 实验要求

* [实验4：Simulink仿真PID控制](./Experiments/Exp4：Simulink仿真PID控制)
  * [源文件](./Experiments/Exp4：Simulink仿真PID控制/Code)
    * PID控制模型：[`PID控制模型.slx`](./Experiments/Exp4：Simulink仿真PID控制/Code/PID控制模型.slx)
    * 动图代码：[`PID_Drow.m`](./Experiments/Exp4：Simulink仿真PID控制/Code/PID_Drow.m)
  * 动图效果：[PID曲线变化过程.mp4](。/Experiments/Exp4：Simulink仿真PID控制/PID曲线变化过程.mp4)
  * 实验报告：[Report.docx](./Experiments/Exp4：Simulink仿真PID控制/Report.docx)
  * 实验要求：[实验要求.docx](./Experiments/Exp4：Simulink仿真PID控制/实验要求.docx)
