__doc__ = """工具函函数"""

import random

import matplotlib
import pandas as pd
import torch
import torch_geometric.utils
from matplotlib import pyplot as plt

from configs import ITERS_PER_EVAL

matplotlib.use('TkAgg')


def loadNodes(csv_path: str, index_col: str) -> dict:
    """加载包含节点信息的csv文件
    :param csv_path: csv文件路径
    :param index_col: index所在列的列名
    :return: dict[int: int], 原id到新id的映射
    """
    df = pd.read_csv(csv_path, index_col=index_col)
    mapping = {index: i for i, index in enumerate(df.index.unique())}
    return mapping


def loadEdges(csv_path: str, user_mapping: dict, anime_mapping: dict, user_id_col: str = 'user_id',
              anime_index_col: str = 'item_id', link_index_col: str = 'rating', rating_threshold: int = 4):
    """加载包含用户和项目之间的边的csv文件
    :param csv_path: rating csv文件路径
    :param user_id_col: used_id在rating文件中的列名，本数据集中为"user_id"
    :param user_mapping: user_id到新id(0~n)的映射
    :param anime_index_col: anime_id在rating文件中的列名，本数据集中为"item_id"
    :param anime_mapping: anime_id到新id(0~n)的映射
    :param link_index_col: 用户-项 之间的关联的列名
    :param rating_threshold: 评分阈值，大于等于该阈值的边才将被保留
    :return: torch.Tensor: 2 by N matrix containing the node ids of N user-item edges
    """
    rating_df = pd.read_csv(csv_path)  # rating文件

    src = [user_mapping[index] for index in rating_df[user_id_col]]  # 新user_id
    # 鉴于有的anime在rating中但不在anime中，所以下面用None填充
    dst = [anime_mapping[index] if index in anime_mapping else None for index in
           rating_df[anime_index_col]]  # 新anime_id

    # 利用rating的高低作为edge_attr；数据类型转换：np[ndarray]->torch.Tensor[long]；维度转换：(1, n) -> (n, 1)
    edge_attr = torch.from_numpy(rating_df[link_index_col].values).view(-1, 1).to(torch.long) >= rating_threshold

    edge_index = [[], []]  # 合并 src dst 为 COO 格式
    for i in range(edge_attr.shape[0]):
        if edge_attr[i] and dst[i] is not None:
            edge_index[0].append(src[i])
            edge_index[1].append(dst[i])

    return torch.tensor(edge_index)  # 从list转为torch.Tensor


def getOriginID(mapping, new_id) -> int:
    """
    从新ID获取旧ID(实质是根据新id(value)找旧id(key))
    :param mapping: 通过loadNodes()得到的映射
    :param new_id: 新id(value)
    :return: 旧id(key)
    """
    for key, value in mapping.items():
        if value == new_id:
            return key


# helper function to get N_u
def getUserPositiveItems(edge_index):
    """为每个用户生成正采样字典
    :param: edge_index (torch.Tensor): 2*N的边列表
    :return: dict: 每个用户的正采样字典
    """
    user_pos_items = {}
    for i in range(edge_index.shape[1]):
        user = edge_index[0][i].item()
        item = edge_index[1][i].item()
        if user not in user_pos_items:
            user_pos_items[user] = []
        user_pos_items[user].append(item)
    return user_pos_items


def plotLoss(train_losses: list, val_losses: list):
    """绘制训练和验证损失曲线
    :param train_losses: 训练损失
    :param val_losses: 验证损失
    """
    iters = [iter * ITERS_PER_EVAL for iter in range(len(train_losses))]

    plt.subplot(2, 1, 1)
    plt.plot(iters, train_losses, label='train')
    plt.xlabel('iteration')
    plt.ylabel('loss')
    plt.title("Training loss")

    plt.subplot(2, 1, 2)
    plt.plot(iters, val_losses, label='validation')
    plt.xlabel('iteration')
    plt.ylabel('loss')
    plt.title("Validation loss")

    plt.suptitle('Training and Validation loss curves')
    plt.show()


def miniBatchSample(batch_size, edge_index):
    """随机抽取正负样本
    :param batch_size: 批大小
    :param edge_index: 二部图的边集
    :return: 用户索引, 正样本索引, 负样本索引
    """
    # 为了计算BPR loss，需要手动生成负权边
    edges = torch_geometric.utils.structured_negative_sampling(edge_index=edge_index)
    edges = torch.stack(edges, dim=0)
    indices = random.choices([i for i in range(edges[0].shape[0])], k=batch_size)
    batch = edges[:, indices]
    users_idx, pos_items_idx, neg_items_idx = batch[0], batch[1], batch[2]
    return users_idx, pos_items_idx, neg_items_idx
