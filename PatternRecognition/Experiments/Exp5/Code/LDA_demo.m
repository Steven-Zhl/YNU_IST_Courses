%读取数据
fileID = fopen("Iris.data"); % 打开文件
data = textscan(fileID, '%f%f%f%f%s', 'Delimiter', ',');
attrib = [data{1, 1}, data{1, 2}, data{1, 3}, data{1, 4}];
class = data{1, 5};
X = attrib(1:150, :); % 读取共150条数据
label_set = char('Iris-setosa', 'Iris-versicolor', 'Iris-virginica');
label = zeros(100, 1);
label(strcmp(class, 'Iris-setosa')) = 1;
label(strcmp(class, 'Iris-versicolor')) = 2;
label(strcmp(class, 'Iris-virginica')) = 3;

[vec, val] = LDA(X', label); % 计算
% 降维
X = X * vec(:, 1:2);
% 画散点图
figure;
scatter(X(1:50, 1), X(1:50, 2), 'r', 'LineWidth', 2);
hold on;
scatter(X(51:100, 1), X(51:100, 2), 'g', 'LineWidth', 2);
hold on;
scatter(X(101:150, 1), X(101:150, 2), 'b', 'LineWidth', 2);
hold on;
legend('Iris-setosa', 'Iris-versicolor', 'Iris-virginica');
title('LDA');
xlabel('$x_1$', 'Interpreter', 'latex');
ylabel('$x_2$', 'Interpreter', 'latex');

function [vec, val] = LDA(xtr, ytr)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Input:
    %     xtr:  data matrix (Each column is a data point)
    %     ytr:  class label (class 1, ..., k)
    % Output:
    %     vec:  sorted discriminative components
    %     val:  corresponding eigenvalues
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%

    [D, ntr] = size(xtr);
    classnum = length(unique(ytr));
    miu = mean(xtr, 2);

    sigmaB = sparse(D, D);
    miu_class = zeros(size(xtr, 1), classnum);

    for i = 1:classnum
        miu_class(:, i) = mean(xtr(:, ytr == i), 2);
        sigmaB = sigmaB + length(find(ytr == i)) * (miu_class(:, i) - miu) * (miu_class(:, i) - miu)';
    end

    sigmaB = (sigmaB + sigmaB') / 2;

    sigmaT = (ntr - 1) * cov(xtr');
    sigmaT = (sigmaT + sigmaT') / 2;

    sigmaW = sigmaT - sigmaB;
    sigmaW = (sigmaW + sigmaW') / 2;

    [eigvector, eigvalue] = eig(sigmaB, sigmaW);
    [val, id] = sort(-diag(eigvalue));
    vec = eigvector(:, id);
    val = -val;
end
