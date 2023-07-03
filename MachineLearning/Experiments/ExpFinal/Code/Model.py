import numpy as np
import torch
from torch import nn, Tensor
from torch_geometric.nn.conv import MessagePassing
from torch_geometric.nn.conv.gcn_conv import gcn_norm
from torch_geometric.utils import structured_negative_sampling
from torch_sparse import SparseTensor, matmul

from utils import getUserPositiveItems


class LightGCN(MessagePassing):
    """LightGCN Model：https://arxiv.org/abs/2002.02126"""

    def __init__(self, num_users, num_animes, embedding_dim=64, K=3, add_self_loops=False, **kwargs):
        """定义LightGCN 模型
        :param num_users: 用户数量
        :param num_animes: 动画数量
        :param embedding_dim: 嵌入维度，默认 64，后续可以调整观察效果
        :param K: Message Passing 层数，默认 3
        :param add_self_loops: 传递时是否添加结点自身，默认 False
        """
        kwargs.setdefault('aggr', 'add')  # 聚合方式
        super().__init__(**kwargs)
        self.num_users, self.num_animes = num_users, num_animes
        self.embedding_dim, self.K = embedding_dim, K
        self.add_self_loops = add_self_loops

        self.users_emb = nn.Embedding(num_embeddings=self.num_users, embedding_dim=self.embedding_dim)  # e_u^0
        self.animes_emb = nn.Embedding(num_embeddings=self.num_animes, embedding_dim=self.embedding_dim)  # e_i^0

        # 初始化 Embedding
        nn.init.normal_(self.users_emb.weight, std=0.1)
        nn.init.normal_(self.animes_emb.weight, std=0.1)

    def forward(self, edge_index: SparseTensor):
        """正向传播
        :param edge_index: adjacency matrix
        :return: tuple (Tensor): `e_u_k`, `e_u_0`, `e_i_k`, `e_i_0`
        """
        # 使用gcn_norm计算A=DAD，且加入了 self_loops
        edge_index_norm = gcn_norm(edge_index, add_self_loops=self.add_self_loops)

        emb_0 = torch.cat([self.users_emb.weight, self.animes_emb.weight])  # E^0
        embs = [emb_0]
        emb_k = emb_0

        # 计算 propagation (Wx+b)
        for i in range(self.K):
            emb_k = self.propagate(edge_index_norm, x=emb_k)
            embs.append(emb_k)

        embs = torch.stack(embs, dim=1)
        emb_final = torch.mean(embs, dim=1)  # E^K

        # 把 user item 的特征分量分开
        users_emb_final, items_emb_final = torch.split(emb_final, [self.num_users, self.num_animes])

        # returns e_u^K, e_u^0, e_i^K, e_i^0
        return users_emb_final, self.users_emb.weight, items_emb_final, self.animes_emb.weight

    def message(self, x_j: Tensor) -> Tensor:
        return x_j

    def message_and_aggregate(self, adj_t: SparseTensor, x: Tensor) -> Tensor:
        """
        :param adj_t: 邻接矩阵(转置)
        """
        # \tilde{A} @ x
        return matmul(adj_t, x)

    def evaluation(self, edge_index, sparse_edge_index, exclude_edge_indices, k, lambda_val):
        users_emb_final, users_emb_0, items_emb_final, items_emb_0 = self.forward(sparse_edge_index)
        edges = structured_negative_sampling(edge_index, contains_neg_self_loops=False)
        user_indices, pos_item_indices, neg_item_indices = edges[0], edges[1], edges[2]
        users_emb_final, users_emb_0 = users_emb_final[user_indices], users_emb_0[user_indices]
        pos_items_emb_final, pos_items_emb_0 = items_emb_final[pos_item_indices], items_emb_0[pos_item_indices]
        neg_items_emb_final, neg_items_emb_0 = items_emb_final[neg_item_indices], items_emb_0[neg_item_indices]

        loss = self.BPR_loss(users_emb_final, users_emb_0, pos_items_emb_final, pos_items_emb_0, neg_items_emb_final,
                             neg_items_emb_0, lambda_val).item()

        recall, precision, ndcg = self.getMetrics(edge_index, exclude_edge_indices, k)

        return loss, recall, precision, ndcg

    def getMetrics(self, edge_index, exclude_edge_indices, k):
        """计算查全率、查准率和NDCG
        :params: model (LighGCN): lightgcn model
        :params: edge_index (torch.Tensor): 2*N列表
        :params: exclude_edge_indices ([type]): 2*N列表
        :params: k (int): 前多少个电影
        :return: tuple: recall @ k, precision @ k, ndcg @ k
        """
        user_embedding = self.users_emb.weight
        item_embedding = self.animes_emb.weight
        # 获取每个用户和动画之间的评分 - shape是num users x num animes
        rating = torch.matmul(user_embedding, item_embedding.T)

        for exclude_edge_index in exclude_edge_indices:
            # 获取每个用户的正向评分项
            user_pos_items = getUserPositiveItems(exclude_edge_index)
            exclude_users = []
            exclude_items = []
            for user, items in user_pos_items.items():
                exclude_users.extend([user] * len(items))
                exclude_items.extend(items)
            rating[exclude_users, exclude_items] = -(1 << 10)

        _, top_K_items = torch.topk(rating, k=k)  # 获取每个用户的前k个推荐项
        users = edge_index[0].unique()
        test_user_pos_items = getUserPositiveItems(edge_index)
        # 将测试用户正向评分项字典转换为列表
        test_user_pos_items_list = [test_user_pos_items[user.item()] for user in users]
        # 确定每个用户的前k个推荐项是否在其正向评分项中
        r = []
        for user in users:
            ground_truth_items = test_user_pos_items[user.item()]
            label = list(map(lambda x: x in ground_truth_items, top_K_items[user]))
            r.append(label)
        r = torch.Tensor(np.array(r).astype('float'))

        recall, precision = self.recallPrecision_k(test_user_pos_items_list, r, k)
        ndcg = self.NDCG_K_r(test_user_pos_items_list, r, k)

        return recall, precision, ndcg

    def BPR_loss(self, users_emb_final, users_emb_0, pos_items_emb_final, pos_items_emb_0, neg_items_emb_final,
                 neg_items_emb_0, lambda_val):
        """Bayesian Personalized Ranking Loss： https://arxiv.org/abs/1205.2618
        :param users_emb_final: e_u_k
        :param users_emb_0: e_u_0
        :param pos_items_emb_final: positive e_i_k
        :param pos_items_emb_0: positive e_i_0
        :param neg_items_emb_final: negative e_i_k
        :param neg_items_emb_0: negative e_i_0
        :param lambda_val: 正则化损失项的lambda值
        :return: BPR损失
        """
        reg_loss = lambda_val * (users_emb_0.norm(2).pow(2) +
                                 pos_items_emb_0.norm(2).pow(2) +
                                 neg_items_emb_0.norm(2).pow(2))  # L2 loss

        pos_scores = torch.mul(users_emb_final, pos_items_emb_final)
        pos_scores = torch.sum(pos_scores, dim=-1)  # positive samples的预测得分
        neg_scores = torch.mul(users_emb_final, neg_items_emb_final)
        neg_scores = torch.sum(neg_scores, dim=-1)  # negative samples的预测得分

        loss = -torch.mean(torch.nn.functional.softplus(pos_scores - neg_scores)) + reg_loss

        return loss

    def recallPrecision_k(self, groundTruth, r, k):
        """
        :param: groundTruth (list): 每个用户对应电影列表的高评分项
        :param: r (Tensor): 是否向每个用户推荐了前k个电影的列表
        :param: k (intg): 确定要计算精度和召回率的前k个电影
        :return: tuple: recall @ k, precision @ k
        """
        num_correct_pred = torch.sum(r, dim=-1)  # 每个用户预测正确的数目number of correctly predicted items per user
        user_num_liked = torch.Tensor([len(groundTruth[i]) for i in range(len(groundTruth))])
        recall = torch.mean(num_correct_pred / user_num_liked)
        precision = torch.mean(num_correct_pred) / k
        return recall.item(), precision.item()

    def NDCG_K_r(self, groundTruth, r, k):
        """计算归一化折扣累计收益(Normalized Discounted Cumulative Gain/NDCG) @ k
        :param: groundTruth (list): 同上一个函数
        :param: r (list): 同上一个函数
        :param: k (int): 同上一个函数
        :return: float: ndcg @ k
        """
        assert len(r) == len(groundTruth)

        test_matrix = torch.zeros((len(r), k))
        for i, items in enumerate(groundTruth):
            length = min(len(items), k)
            test_matrix[i, :length] = 1
        max_r = test_matrix
        idcg = torch.sum(max_r * 1. / torch.log2(torch.arange(2, k + 2)), axis=1)
        dcg = r * (1. / torch.log2(torch.arange(2, k + 2)))
        dcg = torch.sum(dcg, axis=1)
        idcg[idcg == 0.] = 1.
        ndcg = dcg / idcg
        ndcg[torch.isnan(ndcg)] = 0.
        return torch.mean(ndcg).item()
