import torch
import torch.optim as optim
from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms
from torchvision.datasets import CIFAR10

device = "cuda:0" if torch.cuda.is_available() else "cpu"
# 设定超参数
BATCH_SIZE = 64  # 设定每一个Batch的大小
EPOCHS = 15  # 迭代次数


# 定义AlexNet模型
class AlexNet(nn.Module):
    def __init__(self) -> None:
        super(AlexNet, self).__init__()
        # Cov2d参数分别为：输入通道数，输出通道数，卷积核大小，步长，填充
        self.conv1 = nn.Sequential(nn.Conv2d(3, 96, 11, 4, 2), nn.ReLU(), nn.MaxPool2d(3, 2))
        self.conv2 = nn.Sequential(nn.Conv2d(96, 256, 5, 1, 2), nn.ReLU(), nn.MaxPool2d(3, 2))
        self.conv3 = nn.Sequential(nn.Conv2d(256, 384, 3, 1, 1), nn.ReLU())
        self.conv4 = nn.Sequential(nn.Conv2d(384, 384, 3, 1, 1), nn.ReLU())
        self.conv5 = nn.Sequential(nn.Conv2d(384, 256, 3, 1, 1), nn.ReLU(), nn.MaxPool2d(3, 2))
        self.fc1 = nn.Sequential(nn.Linear(256 * 6 * 6, 4096), nn.ReLU(), nn.Dropout(0.5))
        self.fc2 = nn.Sequential(nn.Linear(4096, 4096), nn.ReLU(), nn.Dropout(0.5))
        self.fc3 = nn.Linear(4096, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = x.view(x.shape[0], -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x


if __name__ == "__main__":
    # 数据预处理
    dataPath = "/home/MachineLeaerning/Exp5/Data"  # 数据集路径，填写'cifar-10-batches-py'文件夹的上级路径(不确定相对路径行不行，所以建议写绝对路径)
    transform = transforms.Compose([transforms.ToTensor(), transforms.Resize(224), transforms.RandomHorizontalFlip(),
                                    transforms.Normalize(mean=[0.5], std=[0.5])])
    trainData = CIFAR10(dataPath, train=True, transform=transform, download=False)  # 下载训练集和测试集
    testData = CIFAR10(dataPath, train=False, transform=transform, download=False)
    trainDataLoader = DataLoader(dataset=trainData, batch_size=BATCH_SIZE, shuffle=True)  # 构建数据集和测试集的DataLoader
    testDataLoader = DataLoader(dataset=testData, batch_size=BATCH_SIZE, shuffle=False)
    classes = ("Airplane", "Car", "Bird", "Cat", "Deer", "Dog", "Frog", "Horse", "Ship", "Truck")

    # AlexNet
    # 实例化网络、优化器、损失函数
    net = AlexNet().to(device)  # 实例化网络
    optimizer = optim.Adam(net.parameters())  # 实例化优化器
    criterion = nn.CrossEntropyLoss()  # 实例化损失函数
    # 训练模型，并使用tensorboard可视化
    writer = SummaryWriter(log_dir="AlexNet_Logs")
    for epoch in range(EPOCHS):
        for i, data in enumerate(trainDataLoader, 0):
            inputs, labels = data
            inputs = inputs.cuda()
            labels = labels.cuda()
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            writer.add_scalar("loss", loss.item(), epoch * len(trainDataLoader) + i)
    # 保存模型
    torch.save(net.state_dict(), "AlexNet.pth")
