from math import inf as I


def changes_arrangement(n, changes: list = None):
    """
    使用贪心思想，求解最小张数的找零方案，及对应张数
    当然，众所周知，贪心思想不一定能求得最优解
    :param n: 找零金额
    :param changes: 零钱面额，升序排列，且认为所有零钱数量都是无限的
    :return: 贪心算法计算的最小找零张数，及对应的找零方案
    """
    changes = [1, 5, 10, 20, 50, 100] if changes is None else changes
    # 默认的零钱面额情况
    changes.sort()  # 升序排列
    res = []  # 找零方案
    i = len(changes) - 1  # 一个计数器，表示从面值最大的零钱开始考虑
    while n != 0:  # 停止条件
        if n >= changes[i]:  # 应找的零钱比当前大
            n = n - changes[i]
            res.append(changes[i])
        else:  # 当前零钱大于应找的面额，则应重新考虑找零面额
            i = i - 1
    return len(res), res


def Kruskal(graph):
    """
    使用Kruskal算法求解最小生成树
    :param graph: 邻接矩阵，不存在边的边权用I(inf)代替
    :return: 最小生成树（所有边）
    """
    # 最小生成树的边集，每个边都使用[边权, 边起点, 边终点]的三元组的表示形式
    tree = []
    # 原图的点集、边集
    Vex, Edge = set([i for i in range(len(graph))]), []
    # 边集初始化
    for row in range(len(graph)):
        for col in range(row + 1, len(graph)):
            if graph[row][col] != I:
                Edge.append([graph[row][col], row, col])
    Edge.sort(key=lambda i: i[0])  # 按照升序排列
    # 将最小边放入最小生成树
    tree.append(Edge.pop(0))
    Vex = Vex - {tree[-1][1], tree[-1][2]}  # 更新Vex，即删去取出的边对应的两点
    while len(tree) != len(graph) - 1:
        for i in Edge:
            if (i[1] not in Vex and i[2] in Vex) or (i[1] in Vex and i[2] not in Vex):  # 判断是否成环
                tree.append(i)
                Vex.remove(i[1] if i[1] in Vex else i[2])
                Edge.remove(i)
                break
    return tree


def Kruskal_reverse(graph):
    """
    使用Kruskal算法求解最大生成树
    :param graph: 邻接矩阵，不存在边的边权用I(inf)代替
    :return: 最大生成树（所有边）
    """
    # 最大生成树的边集，每个边都使用[边权, 边起点, 边终点]的三元组的表示形式
    tree = []
    # 原图的点集、边集
    Vex, Edge = set([i for i in range(len(graph))]), []
    # 边集初始化
    for row in range(len(graph)):
        for col in range(row + 1, len(graph)):
            if graph[row][col] != I:
                Edge.append([graph[row][col], row, col])
    Edge.sort(key=lambda i: i[0], reverse=True)  # 按照降序排列
    # 将最大边放入最大生成树
    tree.append(Edge.pop(0))
    Vex = Vex - {tree[-1][1], tree[-1][2]}  # 更新Vex，即删去取出的边对应的两点
    while len(tree) != len(graph) - 1:
        for i in Edge:
            if (i[1] not in Vex and i[2] in Vex) or (i[1] in Vex and i[2] not in Vex):  # 判断是否成环
                tree.append(i)
                Vex.remove(i[1] if i[1] in Vex else i[2])
                Edge.remove(i)
                break
    return tree


graph = [[0, 5, I, 6, I],
         [5, 0, 1, 3, I],
         [I, 1, 0, 4, 6],
         [6, 3, 4, 0, 2],
         [I, I, 6, 2, 0]
         ]

print(Kruskal_reverse(graph))
