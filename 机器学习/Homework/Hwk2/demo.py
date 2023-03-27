# 以Python风格伪代码表示非递归决策树生成算法
class Node:
    def __init__(self, D, A):
        self.D = D
        self.A = A


D = {(X1, y1), (X2, y2), ..., (Xn, yn)}  # 训练集
A = {a1, a2, ..., am}  # 属性集


def TreeGenerate(D, A):
    queue = [Node(D, A)]  # 生成队列并将结点加入队列
    while queue:
        root = queue.pop(0)  # 从队列中取出结点

        if D中样本全属于同一类别C:
            root.type = C
            root.is_leaf = True
            return root
        if A is None or D中样本在A上取值相同:
            root.type = max(count(D.type))  # 选择D中样本数最多的类别
            root.is_leaf = True
            return root
        attr_best = A.best_attr()  # 选择最优划分属性
        for attr_v in attr_best.values:  # 遍历最优划分属性的每个取值
            Dv = D[attr_v]  # 生成Dv
            node_branch = Node(Dv, A-{attr_best})  # 生成新结点
            if Dv is None:
                node_branch.type = max(count(D.type))  # 标记为D中样本数最多的类别
                node_branch.is_leaf = True
                root.children.append(node_branch)  # 构建树
            else:
                root.children.append(node_branch)
                queue.append(node_branch)  # 将新结点加入队列，下次while将会从该结点开始继续构建树

    return root


if __name__ == '__main__':
    TreeGenerate(D, A)
