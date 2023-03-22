import matplotlib
import numpy as np
from pandas import read_csv
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score

__doc__ = """
经过最近的尝试与深刻反省，决定重写Exp1源代码regression.py，新版本为Vol1.1和Vol2.0。
原因在于，当前写的代码用于数学运算而非程序设计，首要目标应当是高性能与高可读性，而不必考虑健壮性与(高内聚)低耦合，Jupyter就是个典型的例子。
而在Vol1.0中忽略了这些，盲目封装自己的函数与接口，驼峰和分隔符写法混用，可读性大打折扣的同时性能也无明显优势，故而选择重写，重写的两个版本将大幅降低封装程度。
Vol1.1版本将仍然按照原本的解题方法，第二问选择sklearn.LogisticRegression()完成，能够得到正确的回归结果。
Vol2.0版本将采用手动梯度下降的方式完成，但限于个人能力，未能收敛，仅是迫于实验要求而写的版本，请诸位同仁注意。
当前为Vol1.1。
"""

matplotlib.use('TkAgg')  # 设定绘图后端


def calc_liner_MSE(x: np.ndarray, y: np.ndarray, omega: float, b: float) -> float:
    """
    计算线性回归的均方误差
    :param x: 数据集X
    :param y: 数据集Y
    :param omega: 线性回归函数 斜率
    :param b: 线性回归函数 截距
    :return: 均方误差
    """
    return np.sum(np.power(y - (omega * x + b), 2)) / len(x)  # 为忽略数据集大小造成的影响，这里额外除以len(xData)


def calc_liner_param(x: np.array, y: np.array) -> tuple[float, float]:
    """
    计算线性回归的参数
    :param x: 训练集X(numpy.ndarray)
    :param y: 训练集Y(numpy.ndarray)
    :return: 参数omega和b(线性回归函数中的斜率和截距)
    """
    # 计算参数
    # 根据omega和b的最优解的闭式解，直接计算参数，跳过梯度下降的步骤
    x_avg, y_avg = np.average(x), np.average(y)
    omega = np.sum((x - x_avg) * y) / (np.sum(np.power(x, 2)) - np.power(np.sum(x), 2) / len(x))
    b = y_avg - omega * x_avg
    return omega, b


def liner_regression():
    """
    第一题 线性回归
    :return:None
    """
    # 初始化数据
    df = read_csv('./ex1data1.csv')
    population, profit = df['population'], df['profit']
    # 绘制原始数据的散点图
    canvas1 = plt
    canvas1.scatter(x=population, y=profit, marker='.', color='b', label='Population-Profit', linewidths=3)
    canvas1.legend()
    canvas1.xlabel('Population')
    canvas1.ylabel('Profit')
    canvas1.title('Population-Profit')
    canvas1.show()
    # 计算线性回归参数
    x_train, x_test, y_train, y_test = train_test_split(population, profit, test_size=0.3)
    omega, b = calc_liner_param(x_train, y_train)  # 计算线性回归参数
    # 绘制散点和线性回归函数
    canvas2 = plt
    canvas2.scatter(x=population, y=profit, marker='.', color='b', label='Population-Profit', linewidths=3)
    canvas2.plot(population, omega * population + b, color='r', label=r'$y=%.2fx%.2f$' % (omega, b))
    canvas2.legend()
    canvas2.xlabel('Population')
    canvas2.ylabel('Profit')
    canvas2.title('Population-Profit(with linearRegression)')
    canvas2.show()
    print("训练集均方误差：", calc_liner_MSE(x_train, y_train, omega, b))
    print("测试集均方误差：", calc_liner_MSE(x_test, y_test, omega, b))


def logistic(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression():
    """
    第二题 逻辑回归
    :return: None
    """

    # 初始化数据
    df = read_csv('./ex1data2.csv')
    exam1, exam2, accepted = df['Exam1'], df['Exam2'], df['Accepted']
    x = np.stack((exam1, exam2), axis=1)  # 将二维的exam数据组合起来
    # 建立Logistic模型，使用梯度下降法计算参数
    logistic_model = LogisticRegression(solver='liblinear', C=1e9, max_iter=1000)
    param = logistic_model.fit(x, accepted)  # 训练模型
    print('w=', param.coef_[0], 'b=', param.intercept_)  # 显示模型参数
    print('回归方程为：y=%.2fx1+%.2fx2%.2f' % (param.coef_[0][0], param.coef_[0][1], param.intercept_))
    # 绘制散点和Logistic函数
    x_range, y_range = np.meshgrid(np.linspace(0, 100, 100), np.linspace(0, 100, 100))
    accepted_pred = logistic(param.coef_[0][0] * x_range + param.coef_[0][1] * y_range + param.intercept_)
    canvas = plt
    axis3 = canvas.axes(projection='3d')
    axis3.scatter([exam1[i] for i in range(len(accepted)) if accepted[i] == 1],
                  [exam2[i] for i in range(len(accepted)) if accepted[i] == 1],
                  [1 for i in range(len(accepted)) if accepted[i] == 1],
                  marker='.', label='Admitted', color='green', linewidth=3)  # 画出被录取的散点
    axis3.scatter([exam1[i] for i in range(len(accepted)) if accepted[i] == 0],
                  [exam2[i] for i in range(len(accepted)) if accepted[i] == 0],
                  [0 for i in range(len(accepted)) if accepted[i] == 0],
                  marker='.', label='Not Admitted', color='red', linewidth=3)  # 画出未被录取的散点
    axis3.plot_surface(x_range, y_range, accepted_pred, label='Logistic Regression', color='blue', alpha=0.5)
    axis3.set_xlabel('Exam1')
    axis3.set_ylabel('Exam2')
    axis3.set_zlabel('Admitted')
    canvas.title('Exam1-Exam2-Admitted')
    canvas.show()
    # 五折交叉验证
    precision = cross_val_score(logistic_model, x, accepted, cv=5, scoring='precision')  # 查准率(精确率)
    recall = cross_val_score(logistic_model, x, accepted, cv=5, scoring='recall')  # 查全率(召回率)
    print('五折交叉验证的查准率：', precision)
    print('五折交叉验证的查全率：', recall)


if __name__ == '__main__':
    liner_regression()
    logistic_regression()
