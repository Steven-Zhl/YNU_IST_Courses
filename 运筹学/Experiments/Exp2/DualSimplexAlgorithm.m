%% 算法来自：https://blog.csdn.net/weixin_43727383/article/details/105276545
function [x, y, ResultFlag] = DualSimplexAlgorithm(A, B, C, varargin)
    % 2020-4-2 臻orz
    %inputs:
    %   A:系数矩阵 m*n
    %   B:右端向量 m*1
    %   C:价格系数向量 n*1
    %alternative inputs:
    %   target:优化目标 0 ~ min; 1 ~ max;
    %   sign:约束条件符号 -1 ~ <=; 1 ~ >=;
    %outputs:
    %   x:最优解 n*1
    %   y:最优值 num
    %   ResultFlag:是否找到最优解
    %check inputs
    ip = inputParser;
    ip.addRequired('A', @(x)validateattributes(x, {'double'}, ...
        {'finite', 'nonnan'}, 'BigMSimplexAlgorithm', 'A', 1));
    ip.addRequired('B', @(x)validateattributes(x, {'double'}, ...
        {'size', [size(A, 1), 1]}, 'BigMSimplexAlgorithm', 'B', 2));
    ip.addRequired('C', @(x)validateattributes(x, {'double'}, ...
        {'size', [size(A, 2), 1]}, 'BigMSimplexAlgorithm', 'C', 3));
    ip.addParameter('target', 0, @(x)validateattributes(x, ...
        {'double'}, {'scalar'}, 'BigMSimplexAlgorithm', 'target'));
    ip.addParameter('sign', -1, @(x)validateattributes(x, ...
        {'double'}, {'scalar'}, 'BigMSimplexAlgorithm', 'sign'));
    ip.parse(A, B, C, varargin{:});

    %initialize
    target = ip.Results.target;
    [m, n] = size(A);
    sign = repmat(ip.Results.sign, m, 1);
    P = [];
    x = zeros(n, 1);
    y = 0;
    ResultFlag = 0;
    j = 0;

    %standardization
    if target
        C = -C; %目标函数的转化
    end

    A(B < 0, :) = -A(B < 0, :);
    sign(B < 0, :) = -sign(B < 0, :);
    B = abs(B); %约束条件的转化

    for i = sign'
        j = j + 1;
        switch i
            case -1 %引入松弛变量
                a = zeros(m, 1); a(j) = 1;
                A = [A a];
                C = [C; 0];
            case 1 %引入剩余变量
                A(j, :) = -A(j, :);
                B(j) = -B(j);
                a = zeros(m, 1); a(j) = 1;
                A = [A a];
                C = [C; 0];
        end
    end

    %找寻单位矩阵
    for i = 1:m
        for j = find(A(i, :) == 1)
            if sum(A(:, j) == 0) == m - 1
                P = [P j];
            end
        end
    end

    P = P(1:m);
    CB = C(P); %基变量对应的价值系数
    sigma = C' - CB' * inv(A(:, P)) * A;
    sigma(P) = 0;

    while 1
        if ~sum(B < 0) %有可行解
            x = zeros(size(A, 2), 1);
            x(P) = B;
            x = x(1:n); %舍去引入的松弛变量与剩余变量
            if target
                y = -CB' * B;
            else
                y = CB' * B;
            end
            ResultFlag = 1;
            return;
        end

        for i = find(B < 0)
            if ~sum(A(i, :) < 0)
                return; %无可行解
            end
        end

        pivot_x = find(B == min(B)); %确定主元
        pivot_x = pivot_x(1);
        theta_index = find(A(pivot_x, :) < 0);
        theta = sigma(theta_index) ./ A(pivot_x, theta_index);
        pivot_y = theta_index(theta == max(theta));
        pivot_y = pivot_y(1);
        P(pivot_x) = pivot_y; %更新P
        CB(pivot_x) = C(pivot_y); %更新CB
        %更新系数矩阵
        B(pivot_x) = B(pivot_x) / A(pivot_x, pivot_y);
        A(pivot_x, :) = A(pivot_x, :) ./ A(pivot_x, pivot_y);
        a = 1:m;
        a(pivot_x) = [];

        for i = a
            B(i) = B(i) - A(i, pivot_y) * B(pivot_x);
            A(i, :) = A(i, :) - A(i, pivot_y) * A(pivot_x, :);
        end
        sigma = sigma - sigma(pivot_y) * A(pivot_x, :); %更新sigma
    end
end