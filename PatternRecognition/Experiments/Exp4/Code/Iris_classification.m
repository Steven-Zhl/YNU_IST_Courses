%读取数据
fileID = fopen("Iris.data"); % 打开文件
data = textscan(fileID, '%f%f%f%f%s', 'Delimiter', ',');
attrib1 = data{1, 1}; attrib2 = data{1, 2}; attrib3 = data{1, 3}; attrib4 = data{1, 4}; class = data{1, 5};
attrib = [attrib1, attrib2, attrib3, attrib4];
attrib=attrib(1:100,:); % 前100行恰好是Iris-setosa和Iris-versicolor的样本，因此只读前100行
label_set = char('Iris-setosa', 'Iris-versicolor');
label = zeros(100, 1);
label(strcmp(class, 'Iris-setosa')) = 1;
label(strcmp(class, 'Iris-versicolor')) = -1;

X=attrib;
w0=[0,0,0,0,0];
c=1;
[w,k]=PA(X,w0,c,label);

% 输出w的值和w的迭代更新次数
fprintf('w的值为w(1)=%4.2f, w(2)=%4.2f, w(3)=%4.2f, w(4)=%4.2f, w(5)=%4.2f\n', w(1), w(2), w(3), w(4), w(5));
fprintf('w的迭代更新次数为%d\n', k);

function [W, k] = PA(X, W, c, classes)
    % X为训练样本形成的矩阵，训练样本的个数为N；W为权向量；c为校正增量
    % classes为各训练样本的类别且为一个N维向量，ω1类用1表示，ω2类用-1表示
    [N, n] = size(X); % 训练样本的大小N*n，N即训练样本的个数，n即每个训练样本的维数
    A = ones(N, 1);
    X1 = [X A]; % 将训练样本写成增广向量形式
    % 对训练样本规范化
    for i = 1:N
        X1(i, :) = classes(i) * X1(i, :);
    end

    k = 0; % 迭代次数
    a = 0; % 每一轮迭代中判别函数小于或等于0的个数，即每轮中错判的次数
    b = 0; % 迭代轮数的总数
    b = b + 1;

    for j = 1:N
        if dot(W, X1(j, :), 2) > 0
            k = k + 1;
            W = W;
        else
            a = a + 1;
            W = W + c * X1(j, :);
            k = k + 1;
        end
    end
    while (a >= 1)
        a = 0;
        b = b + 1;
        for j = 1:N
            if dot(W, X1(j, :), 2) > 0
                k = k + 1;
                W = W;
            else
                a = a + 1;
                W = W + c * X1(j, :);
                k = k + 1;
            end
        end
    end
end
