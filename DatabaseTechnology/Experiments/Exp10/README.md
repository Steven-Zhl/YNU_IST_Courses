# SimpleResManager

    这是一个简单的资源管理软件，作为数据库实验期末大作业的分支就到此停止更新了，但其主要分支仍然会继续开发，直到我觉得它足够完善了才会公开。
    我相信这还不是最后。
    唉，说实话这是个很烂的玩意，Bug不少，今天听了一个同学讲了他的项目，我更觉得自己做的东西太烂了。
    现在我会的技术大概还不足以让我做出来这个东西，还是要学习。

## 文件介绍

* [Source](./Source/): Python项目
  * [resource](./Source/resource/): 资源文件夹，包括数据库文件、图标以及界面的ui文件和Python代码
  * [config.json](./Source/config.json): 配置文件，一般仅在程序部署时改动，之后只需代码读取其中的内容
  * [main.py](./Source/main.py): 程序入口
  * [control.py](./Source/control.py): 控制程序，负责协调前后端
  * [file_db.py](./Source/file_db.py): 后端程序，负责读取文件信息和数据库IO
  * [requirements.txt](./Source/requirements.txt): Python依赖列表，使用`pip install -r requirements.txt`安装
* [Image](./Image/): 一些绘制的图与绘图的源文件
* [Documents](./Documents/): 实验要求、实验报告、演示PPT

## 使用方法

* 安装好Python，在命令行中移动到项目根目录，输入`pip install -r requirements.txt`，自动安装依赖；或使用conda等其他包管理器安装依赖。
* 打开根目录下的`config.json`文件，修改`homePageQuickDirs`和`projectPath`的地址为项目在本机的实际路径。
* 在IDE中运行main.py，或直接在Powershell中移动到根目录，输入`python main.py`运行。

## 开发约束

* 不区分K/Ki、M/Mi、G/Gi等单位，统一按照1024(即$2^{10}$)进制来完成
* 在文件大小单位中保留了bit，但鉴于一般文件的最小单位都为byte，所以只认为“bit”为bit(比特)，其他所有可能出现理解冲突的时候都认为是“byte”
* 路径请使用"/"分隔文件层级，并尽量使用绝对路径
* 为了方便，所有的路径都不以"/"结尾
* 路径拼接时请不要使用`os.path.join`，而是直接使用`/`进行连接（因为该函数是默认使用Win的路径格式进行拼接）
* 所有文件均使用UTF-8编码
