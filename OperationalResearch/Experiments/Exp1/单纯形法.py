class 单纯形表:
    def __init__(self, 目标函数: list, 增广矩阵: list):
        self.c = 目标函数
        self.增广矩阵 = 增广矩阵
        self.base_i = []  # 基变量
        self.x_num = len(self.c)  # 有多少个x
        self.iter = 0
        self.sigma = [0] * self.x_num  # 各个x的检验数
        for i in range(len(self.c)):
            if self.c[i] == 0:
                self.base_i.append(i)
        self.calcSigma()
        self.printSheet()

    def printSheet(self):
        """
        输出单纯形表
        :return:
        """
        print("单纯形表" + str(self.iter) + ":")
        print("c_j→", self.c)
        print(["C_B", "基", "b"] + ["x_" + str(i) for i in range(len(self.c))])
        for i in range(len(self.base_i)):
            print(
                [self.c[self.base_i[i]], "x_" + str(self.base_i[i]), (self.增广矩阵[i])[-1]] + (self.增广矩阵[i])[:-1])
        print(["sigma:"] + ['{:.4f}'.format(i) for i in self.sigma])

    def calcSigma(self):
        """
        计算Sigma值以确定换入变量
        :return:
        """
        for i in range(self.x_num):
            if i in self.base_i:
                self.sigma[i] = 0
            else:
                self.sigma[i] = self.c[i] - sum(
                    [self.c[self.base_i[j]] * self.增广矩阵[j][i] for j in range(len(self.base_i))])

    def _calcTheta(self, inIndex):
        """
        计算Theta值以确定换出变量
        :param inIndex:
        :return:
        """
        b = [i[-1] for i in self.增广矩阵]
        theta = [0] * len(b)
        for i in range(len(self.base_i)):
            if self.增广矩阵[i][inIndex] > 0:
                theta[i] = b[i] / self.增广矩阵[i][inIndex]
            else:
                theta[i] = 1.7976931348623157e+308  # 其实是inf，这里用只是为了能在下面的min中排除
        return self.base_i[theta.index(min(theta))]  # 要换出的变量

    def iterCalc(self):
        """
        迭代计算
        :return:
        """
        inIndex = self.sigma.index(max(self.sigma))  # 要换入的变量
        outIndex = self._calcTheta(inIndex)
        print("换入x_" + str(inIndex) + ", 换出x_" + str(outIndex))
        self.base_i[self.base_i.index(outIndex)] = inIndex
        self.增广矩阵[self.base_i.index(inIndex)] = [i / self.增广矩阵[self.base_i.index(inIndex)][inIndex] for i in
                                                 self.增广矩阵[self.base_i.index(inIndex)]]
        for i in range(len(self.增广矩阵)):
            if i != self.base_i.index(inIndex):
                self.增广矩阵[i] = [self.增广矩阵[i][j] - self.增广矩阵[i][inIndex] * self.增广矩阵[self.base_i.index(inIndex)][j] for
                                j in range(len(self.增广矩阵[i]))]
        self.calcSigma()
        self.iter += 1
        self.printSheet()
        if max(self.sigma) > 0:
            self.iterCalc()
        else:
            x = [0] * self.x_num
            b = [i[-1] for i in self.增广矩阵]
            for i in range(self.x_num):
                if i not in self.base_i:
                    x[i] = 0
                else:
                    x[i] = b[self.base_i.index(i)]
            z = sum([self.c[i] * x[i] for i in range(self.x_num)])
            print("最优解为:", x)
            print("目标函数值为:", z)


目标函数 = [2, 3, 0, 0, 0]
增广矩阵 = [[2, 2, 1, 0, 0, 12],
        [4, 0, 0, 1, 0, 16],
        [0, 5, 0, 0, 1, 15]]

a = 单纯形表(目标函数=目标函数, 增广矩阵=增广矩阵)
a.iterCalc()
