import matplotlib
import pandas as pd
import torch
from matplotlib import pyplot as plt
from pandas import read_csv
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

matplotlib.use('TkAgg')
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def init_data(csv_path: str, mode='CPU') -> TensorDataset:
    """
    读取并初始化数据
    :param csv_path: csv文件的路径
    :param mode: 模式，需指定使用CPU或GPU计算，并据此将数据转换为对应类型的tensor类型
    :return: 用TensorDataset包装起来的数据集
    """
    df = read_csv(csv_path)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    if mode == 'GPU':
        X = torch.tensor(X.values, dtype=torch.float32, device=device)
        y = torch.tensor(y.values, dtype=torch.float32, device=device)
    else:
        X = torch.tensor(X.values, dtype=torch.float32)
        y = torch.tensor(y.values, dtype=torch.float32)
    return TensorDataset(X, y)


def train_test_split(data: TensorDataset, test_size=0.2) -> tuple[DataLoader, DataLoader]:
    """
    划分训练集和测试集，并以DataLoader的形式分别返回。由于本次实验均采用20%留出法，所以test_size默认为0.2
    :param data: 原始数据集，需要用TensorDataset的形式包装起来
    :param test_size: 测试集占比，默认0.2
    :return: 依次返回训练集和测试集
    """
    data, test_data = torch.utils.data.random_split(
        data, [len(data) - int(len(data) * test_size), int(len(data) * test_size)])

    train_loader = DataLoader(data, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=16, shuffle=True)
    return train_loader, test_loader


# 线性模型
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.fc1 = nn.Linear(1, 10)  # 输入层，输入维度为1，输出维度为10
        self.fc2 = nn.Linear(10, 10)  # 隐藏层
        self.fc3 = nn.Linear(10, 1)  # 输出层，输出维度重回到1

    def forward(self, x):  # 前向传播时采用relu激活函数
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# 逻辑回归模型
class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(2, 10)  # 输入层，输入维度为2，输出维度为10
        self.fc2 = nn.Linear(10, 10)  # 隐藏层
        self.fc3 = nn.Linear(10, 10)  # 隐藏层
        self.fc4 = nn.Linear(10, 2)  # 输出层，输出维度重回到2

    def forward(self, x):  # 前向传播时采用relu激活函数
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x


def regression():
    """
    第一题：线性回归
    :return: None
    """
    dataset = init_data('./ex1data.csv')  # 读取数据
    # 定义模型、损失函数和优化器
    net = LinearRegression()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.01)
    dataset_train, dataset_test = train_test_split(dataset, 0.2)
    # 训练模型：100个epoch，每个epoch都计算一次训练集和测试集的损失
    loss_train, loss_test = [], []
    for epoch in range(100):
        # 计算训练集损失
        running_loss = 0.0
        for i, data in enumerate(dataset_train):
            X_train, y_train = data
            optimizer.zero_grad()
            y_pred = net(X_train).squeeze()
            loss = criterion(y_pred, y_train)  # 均方误差损失
            loss.backward()  # 反向传播
            optimizer.step()  # 更新参数
            running_loss += loss.item()
        loss_train.append(running_loss / len(dataset_train))  # 记录训练集损失
        running_loss = 0.0  # 重置测试集损失
        with torch.no_grad():  # 测试集仅用于计算损失，不需要反向传播
            for i, data in enumerate(dataset_test):
                X_test, y_test = data
                y_pred = net(X_test).squeeze()  # 预测
                loss = criterion(y_pred, y_test)  # 计算均方差损失
                running_loss += loss.item()
            loss_test.append(running_loss / len(dataset_test))

    # 可视化
    plt.plot(loss_train, label='train', linewidth=3)
    plt.plot(loss_test, label='test', linewidth=3)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()
    # 保存数据
    df = pd.DataFrame({'train': loss_train, 'test': loss_test})
    df.to_csv('Regression loss.csv', index=False)


def classify():
    """
    第二题：逻辑回归
    :return: None
    """
    dataset = init_data('./ex1data2.csv')  # 读取数据
    # 定义模型、损失函数和优化器
    net = Classifier()
    criterion = nn.CrossEntropyLoss()  # 交叉熵损失
    optimizer = optim.Adam(net.parameters(), lr=0.01)
    dataset_train, dataset_test = train_test_split(dataset, 0.2)
    # 训练模型：100个epoch，每个epoch都计算一次训练集和测试集的损失
    loss_train, loss_test = [], []
    for epoch in range(400):
        # 计算训练集损失
        running_loss = 0.0
        for i, data in enumerate(dataset_train):
            X_train, y_train = data
            optimizer.zero_grad()
            y_pred = net(X_train)
            loss = criterion(y_pred.squeeze(), y_train.squeeze().long())  # 交叉熵损失
            loss.backward()  # 反向传播
            optimizer.step()  # 更新参数
            running_loss += loss.item()
        loss_train.append(running_loss / len(dataset_train))  # 记录训练集损失
        correct_num, count_num = 0, 0  # 重置测试集损失
        with torch.no_grad():
            for i, data in enumerate(dataset_test):
                X_test, y_test = data
                y_pred = net(X_test)  # 预测
                _, y_pred = torch.max(y_pred.data, dim=1)
                count_num += y_test.size(0)  # 累加测试集样本数
                correct_num += (y_pred == y_test.squeeze()).sum().item()  # 累加预测正确的样本数
            loss_test.append(1 - correct_num / count_num)  # 记录测试集损失，由于是分类问题，所以直接记录错误率了

    # 可视化
    plt.plot(loss_train, label='train', linewidth=3)
    plt.plot(loss_test, label='test', linewidth=3)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()
    # 保存数据
    df = pd.DataFrame({'train': loss_train, 'test': loss_test})
    df.to_csv('Classification loss.csv', index=False)


if __name__ == "__main__":
    # regression()
    classify()
