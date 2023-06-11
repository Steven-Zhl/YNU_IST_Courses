import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import matplotlib.pyplot as plt
from torch import nn
import torch.optim as optim
#如果网络能在GPU中训练，就使用GPU；否则使用CPU进行训练
device = "cuda:0" if torch.cuda.is_available() else "cpu"


#这个函数包括了两个操作：将图片转换为张量，以及将图片进行归一化处理
transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
                                            # torchvision.transforms.Resize(64),
                                            # torchvision.transforms.RandomCrop(32),
                                   #   torchvision.transforms.RandomHorizontalFlip(),
                                   # torchvision.transforms.ColorJitter(brightness=1),
                                torchvision.transforms.Normalize(mean = [0.5],std = [0.5])])

path = './'  #数据集下载后保存的目录
#下载训练集和测试集
trainData = torchvision.datasets.CIFAR10(path,train = True,transform = transform,download = True)
testData = torchvision.datasets.CIFAR10(path,train = False,transform = transform,download=True)

#设置可调超参数
NETlr= 5e-5#设定学习率
BATCH_SIZE = 64#设定每一个Batch的大小
EPOCHS = 15 #总的循环

#构建数据集和测试集的DataLoader
trainDataLoader = torch.utils.data.DataLoader(dataset = trainData,batch_size = BATCH_SIZE,shuffle = True)
testDataLoader = torch.utils.data.DataLoader(dataset = testData,batch_size = BATCH_SIZE)