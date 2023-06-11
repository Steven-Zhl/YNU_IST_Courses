%----------------------- 本程序为第二章基于最小错误率准则设计贝叶斯分类器的示例代码 -----------------------%
close all;
clear all;
clc;

% x1,x2,x3分别为w1,w2,w3这三个类别的训练样本集，其中每个类别均有3个训练样本，每个样本的维数(特征数，属性数)等于2
x1 = [0, 0; 2, 1; 1, 0]; % w1类的三个训练样本，每行为一个样本
x2 = [-1, 1; -2, 0; -2, -1]; % w2类的三个训练样本，每行为一个样本
x3 = [0, -2; 0, -1; 1, -2]; % w3类的三个训练样本，每行为一个样本

% 求取各类的均值，协方差矩阵及其逆矩阵
u1 = mean(x1); u2 = mean(x2); u3 = mean(x3); % 三类训练样本的均值
c1 = cov(x1); c2 = cov(x2); c3 = cov(x3); % 三类训练样本的协方差矩阵
t1 = diag(c1); t2 = diag(c2); t3 = diag(c3);
c1 = diag(t1); c2 = diag(t2); c3 = diag(t3); % 将三类训练样本的协方差矩阵简化为对角矩阵，这样做是为了满足可逆性，方便后续的求逆操作
inv_c1 = inv(c1); inv_c2 = inv(c2); inv_c3 = inv(c3); % 三类训练样本的协方差矩阵的逆矩阵
d1 = det(c1); d2 = det(c2); d3 = det(c3); % 三类训练样本的协方差矩阵的行列式

% 给定一个测试样本x_test,根据公式(2-39)判断x_test的类别归属
x_test = [-2, 2];
p1 = -0.5 * (x_test - u1) * inv_c1 * (x_test - u1)' - 0.5 * log(d1);
p2 = -0.5 * (x_test - u2) * inv_c2 * (x_test - u2)' - 0.5 * log(d2);
p3 = -0.5 * (x_test - u3) * inv_c3 * (x_test - u3)' - 0.5 * log(d3);
[~, max_id] = max([p1, p2, p3])
fprintf('x_test属于第%d类\n', max_id);

g = str2sym('[x,y]');
g1 = simplify(-0.5 * (g - u1) * inv_c1 * (g - u1)' - 0.5 * log(d1));
g2 = simplify(-0.5 * (g - u2) * inv_c2 * (g - u2)' - 0.5 * log(d2));
g3 = simplify(-0.5 * (g - u3) * inv_c3 * (g - u3)' - 0.5 * log(d3));
g12 = simplify(g1 - g2); % w1,w2类的分界线
g23 = simplify(g2 - g3); % w2,w2类的分界线
g31 = simplify(g3 - g1); % w3,w1类的分界线

% 用不同颜色画出三类分界线
h12 = ezplot(g12); hold on;
set(h12, 'LineWidth', 2, 'color', 'red');
h23 = ezplot(g23); hold on;
set(h23, 'LineWidth', 2, 'color', 'blue');
h31 = ezplot(g31); hold on;
set(h31, 'LineWidth', 2, 'color', 'black');
legend('g12', 'g23', 'g31')

% 用不同颜色和形状画出三类训练样本
plot(x1(1, 1), x1(1, 2), 'or'); hold on;
plot(x1(2, 1), x1(2, 2), 'or'); hold on;
plot(x1(3, 1), x1(3, 2), 'or'); hold on;
plot(x2(1, 1), x2(1, 2), '>b'); hold on;
plot(x2(2, 1), x2(2, 2), '>b'); hold on;
plot(x2(3, 1), x2(3, 2), '>b'); hold on;
plot(x3(1, 1), x3(1, 2), 'vk'); hold on;
plot(x3(2, 1), x3(2, 2), 'vk'); hold on;
plot(x3(3, 1), x3(3, 2), 'vk'); hold on;
title('贝叶斯分类');
xlabel('属性1'); ylabel('属性2');
hold off;
