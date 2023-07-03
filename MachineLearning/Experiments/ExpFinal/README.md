# Anime_LightGCN

> 忙了好久，结果最后答辩拉了....有点烦

* [Anime\_LightGCN](#anime_lightgcn)
  * [环境](#环境)
  * [文件结构](#文件结构)
  * [References](#references)
    * [代码参考](#代码参考)
    * [论文参考](#论文参考)
    * [整体讲解](#整体讲解)
    * [概念细节](#概念细节)

## 环境

* **OS**：EndeavourOS 6.3.9-arch 1-1(Based on ArchLinux)
* **Python**：3.11.3
  * torch：2.0.1+cu118
  * torch_geometric：2.3.1
* **GPU**：NVIDIA RTX 3070(40%采样的数据集会消耗约7.5GB显存)
* **CPU**：Intel Core i5-12600KF
* **RAM**：32GB(40%采样版本会消耗约6GB内存，原始数据版本会消耗约16GB内存)

## 文件结构

* [/mal-anime/](./Code/mal-anime)：存放[mal-anime](https://www.kaggle.com/datasets/shafiwalsher/myanimelist-dataset-2023-top-15000)数据集。但由于显存有限，实际运行时是按照animes采样40%的两个数据集。
* [/model/](./Code/model)：存放模型文件，在我的代码中是每800步保存一次模型。

* [/Model.py](./Code/Model.py)：LightGCN的模型在这里定义
* [/train.py](./Code/train.py)：训练模型
* [/utils.py](./Code/utils.py)：一些工具函数。
* [/predict.py](./Code/predict.py)：调用模型进行预测
* [/sample.py](./Code/sample.py)：对原始数据集进行采样
* [/configs.py](./Code/configs.py)：配置全部存放在这里

## References

### 代码参考

> 这三篇其实基本一致，但是后两篇不全，第一篇最早也最详细，所以建议直接看第一篇。

* [LightGCN with PyTorch Geometric. By Hikaru Hotta and Ada Zhou as part of… | by Ada Zhou | Stanford CS224W GraphML Tutorials | Medium](https://medium.com/stanford-cs224w/lightgcn-with-pytorch-geometric-91bab836471e)
* [LightGCN pytorch 原始碼筆記 | mushding 的小小天地](https://mushding.space/2022/04/28/LightGCN-pytorch-%E5%8E%9F%E5%A7%8B%E7%A2%BC%E7%AD%86%E8%A8%98/)
* [使用LightGCN实现推荐系统（手撕代码+分析）_推荐系统代码_怀怀怀怀的博客-CSDN博客](https://blog.csdn.net/weixin_44905312/article/details/126140959)

### 论文参考

* [[2002.02126] LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation](https://arxiv.org/abs/2002.02126)
* [LightGCN：用于推荐任务的简化并增强的图卷积网络 SIGIR 2020_BUAA～冬之恋的博客-CSDN博客](https://blog.csdn.net/u013602059/article/details/107792470)
* [Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)

### 整体讲解

* [A Gentle Introduction to Graph Neural Networks](https://distill.pub/2021/gnn-intro/)
* [图卷积网络（GCN）入门详解](https://www.zhihu.com/tardis/zm/art/107162772)
* [零基础多图详解图神经网络（GNN/GCN）【论文精读】_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1iT4y1d7zP)
* [【李沐精读GNN论文总结】A Gentle Introduction to Graph Neural Networks - 知乎](https://zhuanlan.zhihu.com/p/434132221)
* [何时能懂你的心——图卷积神经网络（GCN） - 知乎](https://zhuanlan.zhihu.com/p/71200936)
* [一文让你看懂图卷积神经网络（GCN）！！！ - 知乎](https://zhuanlan.zhihu.com/p/435866777)

### 概念细节

* [怎么形象理解embedding这个概念？ - 知乎](https://www.zhihu.com/question/38002635)
* [图嵌入（Graph embedding）综述 - 知乎](https://zhuanlan.zhihu.com/p/62629465)
* [BPR损失函数 - 知乎](https://zhuanlan.zhihu.com/p/620570517)
