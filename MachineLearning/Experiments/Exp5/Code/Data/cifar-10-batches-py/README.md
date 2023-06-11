# 关于CIFAR-10数据集的一些说明

> 由于CIFAR-10数据集较大，所以不使用git提交。但又因为git无法提交空文件夹，所以使用该文件占位，顺带简单说明一下。

## 如何下载

1. 该文件夹为CIFAR-10数据集的路径，可在[此处](https://www.cs.toronto.edu/~kriz/cifar.html)选择python version下载解压，并将其中的文件放入该文件夹中
2. 在[alexnet.py](../../alexnet.py)的`if "__name__"=="__main__"`部分，你可以看到`CIFAR10`类中有一个参数`download=False`，将其改为`True`即可自动下载并解压CIFAR-10数据集到指定路径下的 **cifar-10-batches-py** 文件夹中。

* 上述两种方式仅限于网络质量较好的情况下(这两种方式都从国外下载，所以可能需要一些“科学上网”)。如果缺乏上述条件，请自行寻找其他下载方式(如Kaggle、国内网盘等)。

## 文件目录

> 该文件夹中的文件结构应如下所示：

    ┗━━━┓ cifar-10-batches-py
        ┣━━━ batches.meta
        ┣━━━ data_batch_1
        ┣━━━ data_batch_2
        ┣━━━ data_batch_3
        ┣━━━ data_batch_4
        ┣━━━ data_batch_5
        ┣━━━ readme.html
        ┗━━━ test_batch

* 其中，readme.html不是必须的
