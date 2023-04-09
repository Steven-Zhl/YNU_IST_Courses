function [mu, sigma] = myNormalMLE(data)
    %% 使用最大似然估计计算正态分布下的标准差和均值
    % 认为矩阵每行为一个样本，每列表示一个维度，即样本为行向量
    mu = sum(data) / size(data, 1); % 矩阵运算，逐列求和除以列数
    sigma = zeros(size(data, 2), size(data, 2)); % 初始化

    for i = 1:size(data, 1)
        sigma = sigma + (data(i, :) - mu) * (data(i, :) - mu)';
    end
    sigma = sigma / size(data, 1);
end
