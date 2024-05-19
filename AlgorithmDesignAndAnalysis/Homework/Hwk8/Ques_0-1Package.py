from numpy import zeros  # 导入下numpy包使用
# 0-1 背包问题
capacity = 6
Weight = [0, 3, 2, 1, 4, 5]  # 为了Weight[i]、Value[i]的i和数学习惯一致，所以在第1列补一个0
Value = [0, 25, 20, 15, 40, 50]


def Ques_0_1Package(capacity, W, V):
    maxval = zeros([len(W), capacity+1])  # 初始化
    for i in range(1, len(W)):  # 考虑到的物品（从1~i）
        for j in range(1, capacity+1):  # 假设的背包容量
            # 因为itme=0或capacity=0的情况已经在初始化的时候被写了，所以不用考虑这种情况了
            if j >= W[i]:
                maxval[i, j] = max(maxval[i-1, j], maxval[i-1, j-W[i]]+V[i])
            elif j < W[i]:
                maxval[i, j] = maxval[i-1, j]
    return maxval


res = Ques0_1Package(capacity=capacity, W=Weight, V=Value)
# index均从0开始
print(res)
