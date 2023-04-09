x = randn(1, 10000);
x(x <- 6) = -6;
x(x > 6) = 6;

px = normpdf(x, 0, 1); % 按照μ=0，σ=1的正态分布计算每个x对应的概率密度函数值
h1 = [0.25, 1, 2, 4, 8]; % 调节参数
N = [1, 16, 256, 2048]; % 样本数
figure; % 创建图窗

for i_h1 = 1:length(h1) % 遍历h1
    h1_offset = (i_h1 - 1) * (numel(N) + 1) + 1; % 绘图位置的偏移量
    subplot(numel(h1), numel(N) + 1, h1_offset);
    plot(x, px, '.');
    ylabel(sprintf('%s%4.2f', 'h1=', h1(i_h1)));
    title('正态分布样本的概率密度函数');

    for i_N = 1:length(N)
        pNx = parzen_GaussWindow(N(i_N), h1(i_h1), x);
        subplot(numel(h1), numel(N) + 1, h1_offset + i_N);
        plot(x, pNx, '.');
        title(sprintf('%s%d', 'N=', N(i_N)));
    end

end

function parzen = parzen_GaussWindow(N, h1, x)
    %% 高斯窗Parzen窗
    % N : 取样个数
    % h1: 用以计算窗函数的宽度
    % x : 数据集
    hN = h1 / sqrt(N); % 计算hN
    parzen = zeros(1, numel(x));

    for u = 1:numel(x) % 遍历每个样本点x(u)，(公式中的X)

        for i = 1:N % 遍历每个取样点x(i)，(公式中的Xi)，通过这个循环完成式⑥中的累加部分
            parzen(u) = parzen(u) + exp((((x(u) - x(i)) / hN)) .^ 2 / -2);
        end

        parzen(u) = parzen(u) / sqrt(2 * pi) / h1 / sqrt(N); % 累加完成之后，再乘以式⑥中Σ前面的部分才得到概率密度
    end

end
