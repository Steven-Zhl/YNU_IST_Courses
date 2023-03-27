import graphviz
import matplotlib.pyplot as plt
import numpy as np
import pandas
from pandas import read_csv
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_graphviz, plot_tree
from sklearn.ensemble import RandomForestClassifier


def init_data(csv_path):
    """
    初始化数据集
    :param csv_path:csv文件路径
    :return:DataFrame形式的数据集
    """
    # 读取数据集
    df = read_csv(csv_path)
    # 填充连续数值
    df['Age'].fillna(df['Age'].mean(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    # 移除无法使用的特征
    df.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1, inplace=True)
    # 编码枚举类型
    df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
    df['Embarked'] = df['Embarked'].map({'S': 0, 'Q': 1, 'C': 2})
    return df


def decision_tree_optimize(data: pandas.DataFrame, optimize: dict = None) -> dict:
    """
    决策树分类器，可选择优化参数
    :param data:读取的数据集
    :param optimize:要优化的参数，如：{'max_depth': range(1, 10), 'min_samples_split': range(2, 10)}
    :return:决策树对象(DecisionTreeClassifier)
    """
    # 划分训练集和测试集
    x = data.drop('Survived', axis=1)
    y = data['Survived']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    if not optimize:
        clf = DecisionTreeClassifier()
        clf.fit(x_train, y_train)
        return {'分类器': clf, '准确率': clf.score(x_test, y_test)}
    else:
        # 使用GridSearchCV选择最优参数
        grid_search = GridSearchCV(DecisionTreeClassifier(), optimize, cv=5)
        grid_search.fit(x_train, y_train)
        clf = DecisionTreeClassifier(**grid_search.best_params_)
        clf.fit(x_train, y_train)
        return {'分类器': clf, '准确率': clf.score(x_test, y_test), '最优参数': grid_search.best_params_}


def decision_tree_cut_branches(data: pandas.DataFrame, cut_branches_mode: str = None) -> dict:
    """
    决策树分类器，可进行剪枝
    :param data:读取的数据集
    :param cut_branches_mode:剪枝类型，可选值：None、'pre'(预剪枝)、'post'(后剪枝)
    :return:决策树对象(DecisionTreeClassifier)
    """
    # 划分训练集和测试集
    x = data.drop('Survived', axis=1)
    y = data['Survived']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    # 创建并训练决策树分类器
    if cut_branches_mode == 'pre':  # 预剪枝
        # 使用GridSearchCV选择最优参数以进行预剪枝
        param_grid = {'max_depth': range(1, 10), 'min_samples_split': range(2, 10)}
        grid_search = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=5)
        grid_search.fit(x_train, y_train)
        clf = DecisionTreeClassifier(**grid_search.best_params_)
    elif cut_branches_mode == 'post':  # 后剪枝
        clf = DecisionTreeClassifier()
        # 计算不同复杂度参数下的最优修剪参数，返回一个字典，包含不同复杂度参数和对应的叶子节点数、不纯度值等信息
        path = clf.cost_complexity_pruning_path(x_train, y_train)
        ccp_alphas = path.ccp_alphas  # 提取出复杂度参数列表
        test_scores = []  # 存储不同复杂度参数下的决策树模型
        for ccp_alpha in ccp_alphas:
            clf = DecisionTreeClassifier(ccp_alpha=ccp_alpha)
            clf.fit(x_train, y_train)
            test_scores.append(clf.score(x_test, y_test))
        # 找出使得验证集上预测精度最高的复杂度参数值
        best_ccp_alpha = ccp_alphas[np.argmax(test_scores)]
        # 使用最佳的复杂度参数值重新建立决策树模型
        clf = DecisionTreeClassifier(ccp_alpha=best_ccp_alpha)
    else:
        raise ValueError('cutOffBranches参数错误')
    clf.fit(x_train, y_train)
    return {'分类器': clf, '准确率': clf.score(x_test, y_test)}


def random_forest_optimize(data: pandas.DataFrame, optimize: dict = None) -> dict:
    """
    随机森林分类器，可选择优化参数
    :param data: 读取的数据集
    :param optimize: 要优化的参数，如{'n_estimators': range(1, 10), 'max_depth': range(1, 10), 'criterion': ['gini', 'entropy']}
    :return:随机森林对象(RandomForestClassifier)
    """
    # 划分训练集和测试集
    x = data.drop('Survived', axis=1)
    y = data['Survived']
    # 由于采用10折交叉验证，所以不需要划分测试集
    if not optimize:
        clf = RandomForestClassifier()
        clf.fit(x, y)
        precision = cross_val_score(clf, x, y, cv=10, scoring='precision').mean()
        recall = cross_val_score(clf, x, y, cv=10, scoring='recall').mean()
        return {'分类器': clf, '查准率': precision, '查全率': recall}
    else:
        # 使用GridSearchCV选择最优参数
        grid_search = GridSearchCV(RandomForestClassifier(), optimize, cv=10)
        grid_search.fit(x, y)
        clf = RandomForestClassifier(**grid_search.best_params_)
        clf.fit(x, y)
        precision = cross_val_score(clf, x, y, cv=10).mean()
        recall = cross_val_score(clf, x, y, cv=10, scoring='recall').mean()
        return {'分类器': clf, '查准率': precision, '查全率': recall, '最优参数': grid_search.best_params_}


def visualize(clf, x, pic_name, draw_mode='graphviz'):
    """
    可视化决策树
    :param clf:决策树分类器对象 
    :param x: 获取特征名称
    :param pic_name: 保存到本地的文件名
    :param draw_mode: 绘图方式，可选值：'graphviz'、'matplotlib'
    :return: None
    """
    if draw_mode == 'graphviz':  # 方法1：使用graphviz
        dot_data = export_graphviz(clf, None, feature_names=x.columns, class_names=['Died', 'Survived'], filled=True)
        graph = graphviz.Source(dot_data)  # 创建图像对象
        graph.render(pic_name, format='pdf')  # 保存图像
    elif draw_mode == 'matplotlib':  # 方法2：使用matplotlib
        plt.figure(figsize=(79, 36))  # 设置图
        plot_tree(clf, feature_names=x.columns, class_names=['Died', 'Survived'], filled=True)
        plt.show()  # 显示图像
    else:
        raise ValueError('draw_mode参数错误')


def decision_tree():
    """
    第一题 决策树
    :return: None
    """
    data = init_data('./ex2data.csv')
    # 第1问
    clf = decision_tree_optimize(data)  # 默认决策树
    clf_max_depth = decision_tree_optimize(data, {'max_depth': range(1, 20)})  # 最大深度
    clf_min_impurity_decrease = decision_tree_optimize(data, {'min_impurity_decrease': np.linspace(0, 1, 100)})  # 最小不纯度
    print('默认决策树准确率：', clf['准确率'])
    print('决策树(最优最大深度)准确率：', clf_max_depth['准确率'], '最优参数：', clf_max_depth['最优参数'])
    print('决策树(最优最小不纯度)准确率：', clf_min_impurity_decrease['准确率'], '最优参数：',
          clf_min_impurity_decrease['最优参数'])
    visualize(clf['分类器'], data.drop('Survived', axis=1), '决策树_默认')
    visualize(clf_max_depth['分类器'], data.drop('Survived', axis=1), '决策树_最大深度')
    visualize(clf_min_impurity_decrease['分类器'], data.drop('Survived', axis=1), '决策树_最小不纯度')
    # 第2问
    clf_pre_cut = decision_tree_cut_branches(data, cut_branches_mode='pre')  # 预剪枝
    clf_post_cut = decision_tree_cut_branches(data, cut_branches_mode='post')  # 后剪枝
    print('决策树(预剪枝)准确率：', clf_pre_cut['准确率'])
    print('决策树(后剪枝)准确率：', clf_post_cut['准确率'])
    visualize(clf_pre_cut['分类器'], data.drop('Survived', axis=1), '决策树_预剪枝')
    visualize(clf_post_cut['分类器'], data.drop('Survived', axis=1), '决策树_后剪枝')


def random_forest():
    """
    第二题 随机森林
    :return: None
    """
    data = init_data('./ex2data.csv')
    clf = random_forest_optimize(data)  # 随机森林
    clf_max_depth = random_forest_optimize(data, {'max_depth': range(1, 20)})  # 最大深度
    clf_n_estimators = random_forest_optimize(data, {'n_estimators': range(1, 100)})  # 树的数量
    clf_criterion = random_forest_optimize(data, {'criterion': ['gini', 'entropy']})  # 分裂结点的标准
    print('随机森林 查准率：', clf['查准率'], '查全率：', clf['查全率'])
    print('随机森林(最优最大深度) 查准率：', clf_max_depth['查准率'], '查全率：', clf_max_depth['查全率'], '最优参数：',
          clf_max_depth['最优参数'])
    print('随机森林(最优树的数量) 查准率：', clf_n_estimators['查准率'], '查全率：', clf_n_estimators['查全率'],
          '最优参数：', clf_n_estimators['最优参数'])
    print('随机森林(最优分裂结点的标准) 查准率：', clf_criterion['查准率'], '查全率：', clf_criterion['查全率'],
          '最优参数：', clf_criterion['最优参数'])
    visualize(clf['分类器'].estimators_[0], data.drop('Survived', axis=1), '随机森林_默认')
    visualize(clf_max_depth['分类器'].estimators_[0], data.drop('Survived', axis=1), '随机森林_最大深度')
    visualize(clf_n_estimators['分类器'].estimators_[0], data.drop('Survived', axis=1), '随机森林_树的数量')
    visualize(clf_criterion['分类器'].estimators_[0], data.drop('Survived', axis=1), '随机森林_分裂结点的标准')


if __name__ == '__main__':
    decision_tree()
    random_forest()
