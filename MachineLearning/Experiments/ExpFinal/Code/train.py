import torch
from sklearn.model_selection import train_test_split
from torch import optim
from torch_sparse import SparseTensor

from Model import LightGCN
from configs import *
from utils import loadNodes, loadEdges, plotLoss, miniBatchSample

# 数据预处理

# 创建user和anime的新旧ID映射(因为原ID不是从0开始且不连续，为便于运算，重新映射)
user_mapping = loadNodes(RATING_PATH, index_col='user_id')  # key: user_id(原id), value: 0~n(新id)
anime_mapping = loadNodes(ANIME_PATH, index_col='anime_id')  # key: anime_id(原id), value: 0~n(新id)

edge = loadEdges(RATING_PATH, user_mapping=user_mapping, anime_mapping=anime_mapping,
                 user_id_col='user_id', anime_index_col='anime_id', link_index_col='rating')  # 2×n，第1行是起点，第2行是终点

# 将边集分为8(训练集)/1(测试集)/1(验证集)
users_num, animes_num = len(user_mapping), len(anime_mapping)
interactions_num = edge.shape[1]  # 二部图的交互数
all_idx = list(range(edge.shape[1]))  # 每条边的索引

train_ids, test_ids = train_test_split(all_idx, test_size=0.2, random_state=1)  # 先划分训练集和测试集
val_ids, test_ids = train_test_split(test_ids, test_size=0.5, random_state=1)  # 再从测试集中划分验证集和测试集

# 划分边集
train_edge, val_edge, test_edge = edge[:, train_ids], edge[:, val_ids], edge[:, test_ids]

# 转换为稀疏张量(矩阵)
train_sparse_edge = SparseTensor(row=train_edge[0], col=train_edge[1],
                                 sparse_sizes=(users_num + animes_num, users_num + animes_num))
val_sparse_edge = SparseTensor(row=val_edge[0], col=val_edge[1],
                               sparse_sizes=(users_num + animes_num, users_num + animes_num))
test_sparse_edge = SparseTensor(row=test_edge[0], col=test_edge[1],
                                sparse_sizes=(users_num + animes_num, users_num + animes_num))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = LightGCN(num_users=users_num, num_animes=animes_num)
model = model.to(device)
model.train()

optimizer = optim.Adam(model.parameters(), lr=LR)
scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)

edge = edge.to(device)
train_edge = train_edge.to(device)
train_sparse_edge = train_sparse_edge.to(device)

val_edge = val_edge.to(device)
val_sparse_edge = val_sparse_edge.to(device)

train_losses = []
val_losses = []
try:
    for iter in range(ITERATIONS):
        users_emb_final, users_emb_0, items_emb_final, items_emb_0 = model.forward(train_sparse_edge)  # 前向传播

        user_indices, pos_item_indices, neg_item_indices = miniBatchSample(BATCH_SIZE, train_edge)
        user_indices, pos_item_indices, neg_item_indices = user_indices.to(device), pos_item_indices.to(device), neg_item_indices.to(device)

        users_emb_final, users_emb_0 = users_emb_final[user_indices], users_emb_0[user_indices]
        pos_items_emb_final, pos_items_emb_0 = items_emb_final[pos_item_indices], items_emb_0[pos_item_indices]
        neg_items_emb_final, neg_items_emb_0 = items_emb_final[neg_item_indices], items_emb_0[neg_item_indices]

        # loss computation
        train_loss = model.BPR_loss(users_emb_final, users_emb_0, pos_items_emb_final, pos_items_emb_0, neg_items_emb_final, neg_items_emb_0, LAMBDA)

        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

        if iter % ITERS_PER_EVAL == 0:
            model.eval()
            val_loss, recall, precision, ndcg = model.evaluation(val_edge, val_sparse_edge, [train_edge], K, LAMBDA)
            print(f"[Iteration {iter}/{ITERATIONS}] train_loss: {round(train_loss.item(), 5)}, val_loss: {round(val_loss, 5)}, val_recall@{K}: {round(recall, 5)}, val_precision@{K}: {round(precision, 5)}, val_ndcg@{K}: {round(ndcg, 5)}")
            train_losses.append(train_loss.item())
            val_losses.append(val_loss)
            if iter % 800 == 0:
                torch.save(model, f"./model/LightGCN_{iter}.pth")  # 保存模型
            model.train()
        if iter % ITERS_PER_LR_DECAY == 0 and iter != 0:
            scheduler.step()
    else:
        torch.save(model, f"./model/LightGCN_{ITERATIONS}.pth")  # 保存模型
        plotLoss(train_losses, val_losses)  # 绘制损失曲线

        model.eval()  # 计算测试集误差
        test_edge = test_edge.to(device)
        test_sparse_edge = test_sparse_edge.to(device)
        test_loss, test_recall, test_precision, test_ndcg = model.evaluation(test_edge, test_sparse_edge, [train_edge, val_edge], K, LAMBDA)
        print(f"test_loss: %2.5f, test_recall@{K}: %2.5f, test_precision@{K}: %2.5f, test_ndcg@{K}: %2.5f" % (test_loss, test_recall, test_precision, test_ndcg))
except KeyboardInterrupt:  # 键盘中断
    plotLoss(train_losses, val_losses)
