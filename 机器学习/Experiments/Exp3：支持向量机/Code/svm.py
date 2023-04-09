import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray
from pandas import read_csv, DataFrame
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC

matplotlib.use('TkAgg')


def init_data(csv_path):
    """
    初始化数据集(鉴于data1和data2的数据格式相同，所以可以使用同一个函数)
    :param csv_path:
    :return:
    """
    df = read_csv(csv_path)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    return X, y


def visualize_linear(clf: SVC, X, y, title):
    """
    可视化数据点和svc(线性核函数)的决策边界
    :param clf: 分类器
    :param X: 数据X，向量
    :param y: 标记y，整型
    :param title: 图片标题
    :return:None
    """
    # 绘制所有散点(因为要求x1纵y1横，所以这里要将X两列对调)
    plt.scatter(X[y == 1].iloc[:, 1], X[y == 1].iloc[:, 0], c='g')
    plt.scatter(X[y == 0].iloc[:, 1], X[y == 0].iloc[:, 0], c='r')
    plt.legend(['a = 1', 'a = 0'])
    omega, b = clf.coef_[0], clf.intercept_[0]  # 获取决策边界的参数w和b
    x_range = np.arange(min(X.iloc[:, 0]), max(X.iloc[:, 0]), 0.1)
    y_range = -(omega[0] * x_range + b) / omega[1]  # 根据决策边界的参数w和b计算y
    plt.plot(y_range, x_range)  # 绘制决策边界
    plt.xlabel('y1')
    plt.ylabel('x1')
    plt.title(title)
    plt.show()


def visualize_nonlinear(clf: SVC, X: ndarray, y: ndarray, title):
    """
    可视化数据点和svc(高斯核函数)的决策边界
    :param clf: 分类器
    :param X: 数据X，向量
    :param y: 标记y，整型
    :param title: 图片标题
    :return:None
    """
    # 分离出a = 1和a = 0的数据
    X_a1 = np.array([X[i] for i in range(len(y)) if y[i] == 1])
    X_a0 = np.array([X[i] for i in range(len(y)) if y[i] == 0])
    # 绘制所有散点(因为要求x1纵y1横，所以这里要将X两列对调)
    plt.scatter(X_a1[:, 1], X_a1[:, 0], c='g')
    plt.scatter(X_a0[:, 1], X_a0[:, 0], c='r')
    plt.legend(['a = 1', 'a = 0'])
    x_range = np.arange(min(X[:, 0]) - 0.01, max(X[:, 0]) + 0.01, 10e-3)
    y_range = np.arange(min(X[:, 1]) - 0.01, max(X[:, 1]) + 0.01, 10e-3)
    x_mesh, y_mesh = np.meshgrid(x_range, y_range)
    z = clf.predict(np.c_[DataFrame(x_mesh.ravel()),
                    DataFrame(y_mesh.ravel())])
    z = z.reshape(x_mesh.shape)
    plt.contourf(y_mesh, x_mesh, z, alpha=0.2)
    plt.xlabel('y1')
    plt.ylabel('x1')
    plt.title(title)
    plt.show()


def svc_linear_kernel(X: DataFrame, y: DataFrame, C_mode: str = 'default') -> tuple:
    """
    构建线性核函数的svc分类器
    :param X: 数据X，向量
    :param y: 标记y，整型
    :param C_mode: 惩罚系数C的类型，'default':默认(1.0)；'random':随机；'best':网格搜索找最优
    :return:(分类器, 在测试集上的准确率)
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    if C_mode == 'default':  # 默认svc分类器, C = 1.0
        clf = SVC(kernel='linear')  # C = 1.0 (default)
        clf.fit(X_train, y_train)
    elif C_mode == 'random':  # C将随机生成
        # uniform()将会生成一个[0, 1)之间的随机数
        clf = SVC(kernel='linear', C=np.random.uniform())
        clf.fit(X_train, y_train)
    elif C_mode == 'best':  # 使用网格搜索，找到最优的C
        grid = GridSearchCV(SVC(kernel='linear'), param_grid={
                            'C': [i / 100 for i in range(1, 101)]}, cv=5)
        grid.fit(X_train, y_train)
        C_best = grid.best_params_['C']
        clf = SVC(kernel='linear', C=C_best)
        clf.fit(X_train, y_train)
    else:
        raise ValueError(
            'Parameter "mode" must be "default", "random" or "best"')
    return clf, clf.score(X_test, y_test)  # 返回分类器和在测试集上的准确率


def svc_nonlinear_kernel(X: ndarray, y: ndarray, gamma_mode: str = 'default') -> tuple:
    """
    构建高斯核函数的svc分类器
    :param X: 数据X，向量
    :param y: 标记y，整型
    :param gamma_mode: 惩罚系数C的类型，'default':默认(1.0)；'auto':自动；'random':随机；'best':网格搜索找最优
    :return:(分类器, 在测试集上的准确率)
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    if gamma_mode == 'default':  # 默认svc分类器, gamma = 1.0
        clf = SVC(kernel='rbf')  # gamma = 1.0 (default)
        clf.fit(X_train, y_train)
    elif gamma_mode == 'auto':  # gamma = 1 / n_features
        clf = SVC(kernel='rbf', gamma='auto')
        clf.fit(X_train, y_train)
    elif gamma_mode == 'random':  # gamma将随机生成
        # uniform()将会生成一个[0, 1)之间的随机数
        clf = SVC(kernel='rbf', gamma=np.random.uniform())
        clf.fit(X_train, y_train)
    elif gamma_mode == 'best':  # 使用网格搜索，找到最优的C
        grid = GridSearchCV(SVC(kernel='rbf'), param_grid={
                            'gamma': [i / 100 for i in range(1, 101)]}, cv=5)
        grid.fit(X_train, y_train)
        gamma_best = grid.best_params_['gamma']
        clf = SVC(kernel='rbf', gamma=gamma_best)
        clf.fit(X_train, y_train)
    else:
        raise ValueError(
            'Parameter "mode" must be "default", "random" or "best"')
    return clf, clf.score(X_test, y_test)  # 返回分类器和在测试集上的准确率


def linear_classify():
    """
    第一题 线性可分类问题，使用线性核函数
    :return: None
    """
    X, y = init_data('ex3data1.csv')
    clf, acc = svc_linear_kernel(X, y)  # svc分类器(默认)及其在测试集上的准确率
    clf_rand, acc_rand = svc_linear_kernel(
        X, y, C_mode='random')  # svc分类器(C随机)及其在测试集上的准确率
    clf_best, acc_best = svc_linear_kernel(
        X, y, C_mode='best')  # svc分类器(C最优)及其在测试集上的准确率
    # 可视化，输出信息
    print('SVC(Default), Accuracy = {:.2%}, C = {:.2f}'.format(acc, clf.C))
    visualize_linear(clf, X, y, title='Decision boundary, Default C = 1.0')
    print('SVC(Random) , Accuracy = {:.2%}, C = {:.2f}'.format(
        acc_rand, clf_rand.C))
    visualize_linear(
        clf_rand, X, y, title='Decision boundary, Random C = {}'.format(clf_rand.C))
    print('SVC(Best)   , Accuracy = {:.2%}, C = {:.2f}'.format(
        acc_best, clf_best.C))
    visualize_linear(
        clf_best, X, y, title='Decision boundary, Best C = {}'.format(clf_best.C))


def nonlinear_classify():
    """
    第二题 线性可分类问题，使用线性核函数
    :return: None
    """
    X, y = init_data('ex3data2.csv')
    X, y = np.array(X), np.array(y)
    clf, acc = svc_nonlinear_kernel(X, y)  # svc分类器(默认)及其在测试集上的准确率
    clf_auto, acc_auto = svc_nonlinear_kernel(
        X, y, gamma_mode='auto')  # svc分类器(gamma自动)及其在测试集上的准确率
    clf_rand, acc_rand = svc_nonlinear_kernel(
        X, y, gamma_mode='random')  # svc分类器(gamma随机)及其在测试集上的准确率
    clf_best, acc_best = svc_nonlinear_kernel(
        X, y, gamma_mode='best')  # svc分类器(gamma最优)及其在测试集上的准确率
    # 可视化并输出信息
    print('SVC(Default), Accuracy = {:.2%}, gamma = {:.2f}'.format(
        acc, 1 / (X.shape[1] * np.var(X))))
    visualize_nonlinear(clf, X, y, title='Decision boundary, Default gamma = {:.2f}'.format(
        1 / (X.shape[1] * np.var(X))))
    print('SVC(Auto)   , Accuracy = {:.2%}, gamma = {:.2f}'.format(
        acc_auto, 1 / X.shape[1]))
    visualize_nonlinear(
        clf_auto, X, y, title='Decision boundary, Auto gamma = {:.2f}'.format(1 / X.shape[1]))
    print('SVC(Random) , Accuracy = {:.2%}, gamma = {:.2f}'.format(
        acc_rand, clf_rand.gamma))
    visualize_nonlinear(
        clf_rand, X, y, title='Decision boundary, Random gamma = {:.2f}'.format(clf_rand.gamma))
    print('SVC(Best)   , Accuracy = {:.2%}, gamma = {:.2f}'.format(
        acc_best, clf_best.gamma))
    visualize_nonlinear(
        clf_best, X, y, title='Decision boundary, Best gamma = {:.2f}'.format(clf_best.gamma))


if __name__ == '__main__':
    linear_classify()
    nonlinear_classify()
