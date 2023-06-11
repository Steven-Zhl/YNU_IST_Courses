from random import choices

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pandas import read_csv

matplotlib.use("TkAgg")
DATA_PATH = "ex6data.csv"


def kmeans(data: np.ndarray, k: int):
    """
    执行聚类算法，返回聚类结果
    :param data: 数据点，每行代表一个数据点，每列代表一个特征
    :param k: 聚类的类别数
    :return:
    """
    mu = choices(data, k=k)  # 随机选择k个均值向量，结果为list[ndarray]
    print(f"聚类数{k}，初始化均值向量µ=\n{mu}")
    iterCount = 0  # 迭代次数
    while True:
        distance = np.zeros((data.shape[0], k))
        for j in range(data.shape[0]):  # 计算每个点到每个均值向量的距离
            for i in range(k):
                distance[j, i] = np.sqrt(np.sum(np.power(data[j] - mu[i], 2)))
        cluster = np.argmin(distance, axis=1)  # 每个点属于哪个类别
        mu_temp = np.zeros((k, data.shape[1]))
        for i in range(k):  # 更新每个类别的均值向量
            mu_temp[i] = np.mean(data[cluster == i], axis=0)
        if np.allclose(mu_temp, mu):  # 如果均值向量不再变化，则停止迭代
            print(f"迭代结束，均值向量µ=\n{mu}")
            break
        else:
            mu = mu_temp
            iterCount += 1
            print(f"第{iterCount}次迭代，均值向量µ=\n{mu}")
    return cluster


def visualize(data: np.ndarray, label: np.ndarray):
    """
    使用散点图可视化聚类结果(仅限二维数据)
    :param data: 数据点
    :param label: 聚类结果
    :return: None
    """
    plt.scatter(data[:, 0].tolist(), data[:, 1].tolist(), c=label, linewidths=3)
    plt.title("K-means Result")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


if __name__ == "__main__":
    data_matrix = np.matrix(read_csv(DATA_PATH))
    labels = kmeans(data_matrix, 3)
    visualize(data_matrix, labels)
