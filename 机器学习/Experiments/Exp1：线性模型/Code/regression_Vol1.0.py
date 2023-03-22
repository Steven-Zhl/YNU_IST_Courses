import csv
import re
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score

__doc__ = """
经过最近的尝试与深刻反省，决定重写Exp1源代码regression.py，新版本为Vol1.1和Vol2.0。
原因在于，当前写的代码用于数学运算而非程序设计，首要目标应当是高性能与高可读性，而不必考虑健壮性与(高内聚)低耦合，Jupyter就是个典型的例子。
而在Vol1.0中忽略了这些，盲目封装自己的函数与接口，驼峰和分隔符写法混用，可读性大打折扣的同时性能也无明显优势，故而选择重写，重写的两个版本将大幅降低封装程度。
Vol1.1版本将仍然按照原本的解题方法，第二问选择sklearn.LogisticRegression()完成，能够得到正确的回归结果。
Vol2.0版本将采用手动梯度下降的方式完成，但限于个人能力，未能收敛，仅是迫于实验要求而写的版本，请诸位同仁注意。
当前为Vol1.0。
"""

# Config: 设定好文件路径和绘图后端
matplotlib.use('TkAgg')
ex1data1 = "./ex1data1.csv"
ex1data2 = "./ex1data2.csv"


def readCSV(fileName, columns: list) -> list[np.ndarray]:
    """
    读取csv文件，依次返回指定的各列数据
    :param fileName:文件绝对路径
    :param columns: 需要读取的列，请使用list按顺序指定每列，从1开始
    :return: Population(np.ndarray)和Profit(np.ndarray)
    """
    # 尝试读取文件
    try:
        with open(fileName, 'rt') as d:
            csv_file = csv.reader(d)
            data = list(csv_file)
    except FileNotFoundError:
        raise FileNotFoundError("文件{fileName}不存在".format(fileName=fileName))
    # 尝试读取第一行，判断数据中是否包含标题行
    try:
        float(data[0][0])  # 判断第一个元素是否为数字
    except ValueError:
        data.pop(0)  # 去掉第一行的标题
    # 读取并转换数据
    columns = columns if columns else [1, 2]
    res = []
    for col in columns:
        res.append(np.array([float(row[col - 1]) for row in data]))  # 因为index是从0开始的
    # 使用pandas.pf.plot()绘图时，绘图结果直接表现为线性的问题，所以这里直接读取数据，转换为float
    return res


# 两个绘图函数
def plotScatter(xData: np.ndarray, yData: np.ndarray, xLabel: str = None, yLabel: str = None, label: str = None,
                title: str = None, handle: plt = None):
    """
    绘制散点图
    :param xData:np.ndarray: X轴数据
    :param yData:np.ndarray: Y轴数据
    :param xLabel:str: X轴标签
    :param yLabel:str: Y轴标签
    :param label:str: 图例
    :param title:str: 图片标题
    :param handle: 画布句柄
    """
    if not handle:
        handle = plt
        handle.figure()
    handle.scatter(x=xData, y=yData, marker='.', color='b', label=label, linewidths=3)
    handle.legend()
    handle.xlabel(xLabel)
    handle.ylabel(yLabel)
    handle.title(title)
    return handle  # 返回句柄，以便于同时绘制多图


def plotLine(xData: np.ndarray, yData: np.ndarray, xLabel: str = None, yLabel: str = None, label: str = None,
             title: str = None, handle: plt = None):
    """
    绘制一条直线
    :param xData:np.ndarray: X轴数据
    :param yData:np.ndarray: Y轴数据
    :param xLabel:str: X轴标签
    :param yLabel:str: Y轴标签
    :param label:str: 图例
    :param title:str: 图片标题
    :param handle: 画布句柄
    """
    if not handle:
        handle = plt
        handle.figure()
    handle.plot(xData, yData, color='r', label=label)
    handle.legend()
    handle.xlabel(xLabel)
    handle.ylabel(yLabel)
    handle.title(title)
    return handle  # 返回句柄，以便于同时绘制多图


def plot3Scatter(xData: np.ndarray, yData: np.ndarray, zData: np.ndarray, xLabel: str = None, yLabel: str = None,
                 zLabel: str = None, label: str = None, title: str = None, color: str = None, handle: plt = None,
                 ax3: plt.axes = None):
    """
    绘制三维散点图
    :param xData:np.ndarray: X轴数据
    :param yData:np.ndarray: Y轴数据
    :param zData:np.ndarray: Z轴数据
    :param xLabel:str: X轴标签
    :param yLabel:str: Y轴标签
    :param zLabel:str: Z轴标签
    :param label:str: 图例
    :param title:str: 图片标题
    :param color:str: 绘图颜色
    :param handle: 画布句柄
    :param ax3: 三维坐标轴句柄
    """
    if not handle:
        handle = plt
        handle.figure()
    if not ax3:
        ax3 = handle.axes(projection='3d')
    ax3.scatter(xData, yData, zData, marker='.', label=label, linewidths=5, color=color)
    ax3.set_xlabel(xLabel)
    ax3.set_ylabel(yLabel)
    ax3.set_zlabel(zLabel)
    handle.title(title)
    return handle, ax3  # 返回句柄，以便于同时绘制多图


def plotSurface(xData: np.ndarray, yData: np.ndarray, zData: np.ndarray, xLabel: str = None, yLabel: str = None,
                zLabel: str = None, label: str = None, title: str = None, handle: plt = None, ax3: plt.axes = None):
    """
    绘制三维曲面图
    :param xData:np.ndarray: X轴数据
    :param yData:np.ndarray: Y轴数据
    :param zData:np.ndarray: Z轴数据
    :param xLabel:str: X轴标签
    :param yLabel:str: Y轴标签
    :param zLabel:str: Z轴标签
    :param label:str: 图例
    :param title:str: 图片标题
    :param handle: 画布句柄
    :param ax3: 三维坐标轴句柄
    """
    if not handle:
        handle = plt
        handle.figure()
    if not ax3:
        ax3 = handle.axes(projection='3d')
    ax3.plot_surface(xData, yData, zData, label=label, cstride=20, rstride=20)
    ax3.set_xlabel(xLabel)
    ax3.set_ylabel(yLabel)
    ax3.set_zlabel(zLabel)
    handle.title(title)
    return handle, ax3  # 返回句柄，以便于同时绘制多图


def splitTrainTest(xData, yData, mode: str, test_size=0.3):
    """
    调用sklearn.model_selection.train_test_split，随机划分训练集和测试集
    :param xData:np.ndarray: 训练集X
    :param yData:np.ndarray: 训练集Y
    :param mode:str: 检验方式，'hold-out':留出法;'k-fold':k折交叉验证,k为整数
    :param test_size: 留出法的测试集占比，默认为0.3
    """
    # 留出法
    if mode == "hold-out":
        return train_test_split(xData, yData, test_size=test_size)
    elif re.match('\d+-fold', mode):
        fold_num = int(mode.split('-')[0])
        num = len(xData) // fold_num  # 每个fold的样本数
        res = []
        for i in range(fold_num):  # 挑选第i个fold作为测试集
            xTrain = [], yTrain = [], xTest = [], yTest = []
            if i == fold_num - 1:  # 最后一个fold，由于num是整除得到的，最后一个fold的样本数超过num个，所以需要特殊处理
                test_index = list(range(i * num, len(xData)))
                train_index = list(range(0, i * num))
                for j in test_index:
                    xTest.append(xData[j])
                    yTest.append(yData[j])
                for j in train_index:
                    xTrain.append(xData[j])
                    yTrain.append(yData[j])
            else:
                test_index = list(range(i * num, (i + 1) * num))
                train_index = list(range(0, i * num)) + list(range((i + 1) * num, len(xData)))
                for j in test_index:
                    xTest.append(xData[j])
                    yTest.append(yData[j])
                for j in train_index:
                    xTrain.append(xData[j])
                    yTrain.append(yData[j])
            res.append({'xTrain': xTrain, 'yTrain': yTrain, 'xTest': xTest, 'yTest': yTest})
        return res


def calcLinerParam(xData: np.array, yData: np.array) -> tuple[float, float]:
    """
    计算线性回归的参数
    :param xData: 训练集X(numpy.ndarray)
    :param yData: 训练集Y(numpy.ndarray)
    :return: 参数omega和b(线性回归函数中的斜率和截距)
    """
    # 计算参数
    # 根据omega和b的最优解的闭式解，直接计算参数，跳过梯度下降的步骤
    xAvg, yAvg = np.average(xData), np.average(yData)
    omega = np.sum((xData - xAvg) * yData) / (np.sum(np.power(xData, 2)) - np.power(np.sum(xData), 2) / len(xData))
    b = yAvg - omega * xAvg
    return omega, b


def calcMSE(xData: np.ndarray, yData: np.ndarray, omega: float, b: float) -> float:
    """
    计算均方误差
    :param xData: 数据集X
    :param yData: 数据集Y
    :param omega: 线性回归函数 斜率
    :param b: 线性回归函数 截距
    :return: 均方误差
    """
    return np.sum(np.power(yData - (omega * xData + b), 2)) / len(xData)  # 为忽略数据集大小造成的影响，这里额外除以len(xData)


def Ques1():
    population, profit = readCSV(ex1data1, columns=[1, 2])  # 读取原始数据
    # 绘制原始数据的散点图
    scatter = plotScatter(xData=population, yData=profit, xLabel="Population", yLabel="Profit",
                          label="Population-Profit", title="Population-Profit Scatter")
    scatter.show()
    # 计算线性回归参数
    X_train, X_test, Y_train, Y_test = splitTrainTest(population, profit, mode='hold-out')  # 划分训练集和测试集
    omega, b = calcLinerParam(X_train, Y_train)  # 计算线性回归参数
    # 绘制散点和线性回归方程图
    scatter_line = plotScatter(population, profit, "Population", "Profit", "Population-Profit")
    scatter_line = plotLine(xData=population, yData=omega * population + b,
                            xLabel="Population", yLabel="Profit", label=r'$y=%.2fx%.2f$' % (omega, b),
                            title="Population-Profit(with linearRegression)", handle=scatter_line)
    scatter_line.show()
    print("训练集均方误差：", calcMSE(X_train, Y_train, omega, b))
    print("测试集均方误差：", calcMSE(X_test, Y_test, omega, b))


def logistic(x):
    return 1 / (1 + np.exp(-x))


def Ques2():
    exam1, exam2, yData = readCSV(ex1data2, [1, 2, 3])  # 读取原始数据
    xData = np.stack((exam1, exam2), axis=1)  # 将二维的exam数据组合起来
    e1_admit, e2_admit, e1_notAdmit, e2_notAdmit = [], [], [], []
    for i in range(len(yData)):
        if yData[i] == 1:
            e1_admit.append(exam1[i])
            e2_admit.append(exam2[i])
        else:
            e1_notAdmit.append(exam1[i])
            e2_notAdmit.append(exam2[i])
    log = LogisticRegression(solver='liblinear', C=1e9, max_iter=1000)  # 建立Logistic模型，使用梯度下降法逼近
    train = log.fit(xData, yData)  # 训练模型
    print('w=', train.coef_[0], 'b=', train.intercept_)  # 显示模型参数
    print('回归方程为：y=%.2fx1+%.2fx2%.2f' % (train.coef_[0][0], train.coef_[0][1], train.intercept_))
    # 在原有数据上绘制logistic函数
    xRange, yRange = np.meshgrid(np.linspace(0, 100, 100), np.linspace(0, 100, 100))
    z = logistic(train.coef_[0][0] * xRange + train.coef_[0][1] * yRange + train.intercept_)
    scatter, ax3 = plot3Scatter(xData=np.array(e1_admit), yData=np.array(e2_admit), zData=np.array([1] * len(e1_admit)),
                                label='Admitted', color='green')
    scatter, ax3 = plot3Scatter(xData=np.array(e1_notAdmit), yData=np.array(e2_notAdmit),
                                zData=np.array([0] * len(e1_notAdmit)),
                                label='Not Admitted', color='red', handle=scatter, ax3=ax3)
    scatter, ax3 = plotSurface(xData=xRange, yData=yRange, zData=z, xLabel="Exam1", yLabel="Exam2", zLabel="Admitted",
                               title="Exam1-Exam2-Admitted Scatter", handle=scatter, ax3=ax3)
    scatter.show()
    # 五折交叉验证
    precision = cross_val_score(log, xData, yData, cv=5, scoring='precision')
    recall = cross_val_score(log, xData, yData, cv=5, scoring='recall')
    print('五折交叉验证的查准率：', precision)
    print('五折交叉验证的查全率：', recall)


if __name__ == '__main__':
    Ques1()
    Ques2()
