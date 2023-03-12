%% 使用: 在命令行内调用函数Exp5(func)，func是不同功能的名字。要将文件和.m文件放在同一路径下。
%% 每题的demo调用格式如下:
% 1. 边缘点检测: Exp5("Ques1");
% 2. 使用光栅扫描跟踪法的边缘线检测: Exp5("Ques2");
% 3. 使用迭代阈值法进行图像分割: Exp5("Ques3");
% 4. 使用质心生长法进行图像分割: Exp5("Ques4");
function Exp5(ques)

    if ques == "Ques1"
        img = im2double(imread("cameraman.tif"));
        img_edge_Roberts = Ques1(img, "Roberts", 0.05);
        img_edge_IsotropySobel = Ques1(img, "IsotropySobel", 0.05);
        img_edge_8_Laplacian = Ques1(img, "8-Laplacian", 0.2);
        img_edge_Kirschs = Ques1(img, "Kirsch", 0.8);
        % 画图
        subplot(3, 4, 1); imshow(img); title("原图");
        subplot(3, 4, 2); imshow(img_edge_Roberts); title("Roberts算子，阈值0.05");
        subplot(3, 4, 3); imshow(img_edge_IsotropySobel); title("各向同性Sobel算子，阈值0.05");
        subplot(3, 4, 4); imshow(img_edge_8_Laplacian); title("8邻域Laplacian算子，阈值0.2");
        for i = 1:8 % 画Kirsch 8方向梯度滤波的图
            subplot(3, 4, i + 4); imshow(img_edge_Kirschs(:, :, i)); title("Kirsch方向梯度，偏转方向: "+num2str(45 * (i - 1))+"°");
        end

    elseif ques == "Ques2"
        img = imread("cameraman.tif");
        img = im2double(img);
        new_img = Ques2(img, 0.2, 0.2);
        imshow(new_img);

    elseif ques == "Ques3"
        img = imread("building.tif");
        img = im2double(img);
        img_res = Ques3(img);
        imshow(img_res);

    elseif ques == "Ques4"
        img = imread("rose_form.tif");
        img = img(:, :, 1);
        new_img = Ques4(img, 98);
        subplot(2, 1, 1); imshow(img); title("原图");
        subplot(2, 2, 3); imshow(new_img(:, :, 1)); title("前景图");
        subplot(2, 2, 4); imshow(new_img(:, :, 2)); title("背景图");
    end

end

%% Ques1: 边缘点检测
% Input/输入:
%   img: 二维矩阵，表示灰度图像
%   filter: 字符串，选择卷积类型，可选类型为"Roberts"、"IsotropySobel"、"8-Laplacian"、"Kirsch"
%   threshold: 阈值，用于在二值化中进行判定
% Output/输出:
%   new_img: 2维灰度矩阵（选择filter == "Kirsch"时是3维灰度矩阵），边缘检测结果
function new_img = Ques1(img, filter, threshold)
    [width, height] = size(img);
    new_img = zeros(size(img));
    % 构建卷积核
    if filter == "Roberts" % Roberts算子
        kernel_h = [-1, 0, 0; 0, 1, 0; 0, 0, 0]; % 水平方向卷积核
        kernel_v = [0, -1, 0; 1, 0, 0; 0, 0, 0]; % 垂直方向卷积核
    elseif filter == "IsotropySobel" % 各向同性Sobel算子
        kernel_h = 1 / (2 + sqrt(2)) * [-1, 0, 1; -sqrt(2), 0, sqrt(2); -1, 0, 1];
        kernel_v = 1 / (2 + sqrt(2)) * [-1, -sqrt(2), -1; 0, 0, 0; 1, sqrt(2), 1];
    elseif filter == "8-Laplacian" % 8邻域Laplacian算子
        kernel = [-1, -1, -1; -1, 8, -1; -1, -1, -1]; % 8邻域拉普拉斯算子
    elseif filter == "Kirsch" % 8方向Kirsch算子
        new_img = zeros([size(img), 8]); % 8方向Kirsch算子需要生成8张图，所以重新定义返回值矩阵为8维
        origin_kernel = [-3, -3, 5; -3, 0, 5; -3, -3, 5];
        kernel = zeros(3, 3, 8);
        for i = 1:8 % 算出8个方向的卷积核
            kernel(:, :, i) = imrotate(origin_kernel, 45 * (i - 1), 'crop');
        end
    else
        disp("边缘点检测算子有误");
        return
    end
    % 进行边缘点检测
    m = 3; n = 3; % 卷积核长宽
    for i = floor(m / 2) + 1:floor(width - m / 2) + 1 % i,j即中心点
        for j = floor(n / 2) + 1:floor(height - n / 2) + 1
            if filter == "Roberts" || filter == "IsotropySobel" % Roberts算子和各向同性Sobel算子
                val_h = sum(sum(img(i - floor(m / 2):i + floor(m / 2), j - floor(n / 2):j + floor(n / 2)) .* kernel_h));
                val_v = sum(sum(img(i - floor(m / 2):i + floor(m / 2), j - floor(n / 2):j + floor(n / 2)) .* kernel_v));
                new_img(i, j) = (val_h > threshold) || (val_v > threshold); % 合并两个方向的结果
            elseif filter == "8-Laplacian" % 8邻域拉普拉斯算子
                val = sum(sum(img(i - floor(m / 2):i + floor(m / 2), j - floor(n / 2):j + floor(n / 2)) .* kernel));
                new_img(i, j) = val > threshold;
            elseif filter == "Kirsch" % 8方向Kirsch算子
                for k = 1:8 % 依次计算8个方向
                    val = sum(sum(img(i - floor(m / 2):i + floor(m / 2), j - floor(n / 2):j + floor(n / 2)) .* kernel(:, :, k)));
                    new_img(i, j, k) = val > threshold;
                end
            end
        end
    end
end

%% Ques2: 使用光栅扫描跟踪法的边缘线检测
% Input/输入:
%   img: 二维矩阵，表示灰度图像
%   threshold_detect: 检测门限（阈值）
%   threshold_track: 跟踪门限（阈值）
% Output/输出:
%   new_img: 2维灰度矩阵，边缘检测结果
function new_img = Ques2(img, threshold_detect, threshold_track)
    new_img = zeros(size(img));
    [width, height] = size(img);
    kernel = [-1, -1, -1; -1, 8, -1; -1, -1, -1]; % 8邻域拉普拉斯算子
    m = 3; n = 3; % 卷积核长宽为3
    % 标记所有的检测点
    for i = floor(m / 2) + 1:floor(width - m / 2) + 1 % i,j即中心点
        for j = floor(n / 2) + 1:floor(height - n / 2) + 1
            val = sum(sum(img(i - floor(m / 2):i + floor(m / 2), j - floor(n / 2):j + floor(n / 2)) .* kernel));
            new_img(i, j) = val > threshold_detect; % 高于检测门限，则进行标记
        end
    end
    % 逐行扫描，检测其下一行的三个邻接像素是否满足跟踪门限
    for i = floor(m / 2) + 1:floor(width - m / 2) + 1 % i,j即中心点
        for j = floor(n / 2) + 1:height - 1
            if new_img(i, j) == 1
                new_img(i + 1, j - 1) = abs(img(i, j) - img(i + 1, j - 1)) >= threshold_track;
                new_img(i + 1, j) = abs(img(i, j) - img(i + 1, j)) >= threshold_track;
                new_img(i + 1, j + 1) = abs(img(i, j) - img(i + 1, j + 1)) >= threshold_track;
            end
        end
    end
end

%% Ques3: 使用迭代阈值法进行图像分割
% Input/输入:
%   img: 二维矩阵，表示灰度图像
% Output/输出:
%   new_img: 2维灰度矩阵，图像分割结果
function new_img = Ques3(img)
    T = mean2(img); %取均值作为初始阈值
    flag = false; % 是否停止迭代
    i = 0;
    % while循环进行迭代
    while ~flag
        renge1 = find(img <= T); %小于阈值的部分
        renge2 = find(img > T); %大于阈值的部分
        T_temp = (mean(img(renge1)) + mean(img(renge2))) / 2; %计算分割后两部分的阈值均值的均值
        flag = (abs(T_temp - T) < 1) || (i >= 30); % 收敛或达到迭代次数上限
        T = T_temp; % 更新T的值
        i = i + 1;
    end
    new_img(renge1) = 0; %将小于阈值的部分赋值为0
    new_img(renge2) = 1; %将大于阈值的部分赋值为1
    new_img = reshape(new_img, size(img)); % 上面两行代码是一维操作，这里将一维向量重新转为二维矩阵
end

%% Ques4: 使用质心生长法进行图像分割 
% Input/输入:
%   img: 灰度图矩阵
%   T: 门限
% Output/输出:
%   new_imgs: 3维灰度矩阵，分别表示前景图和背景图
function new_imgs = Ques4(img, T)
    img = double(img);
    [width, height] = size(img);
    obj = zeros(size(img)); obj(64, 64) = 1; %种子点
    new_imgs = uint8(zeros(width, height, 2));
    flag = true;
    % 迭代
    while flag
        flag = false; % 是否继续迭代
        for i = 2:width - 1
            for j = 2:height - 1
                if obj(i, j) == 1
                    for x = -1:1 % 生长过程
                        for y = -1:1
                            if obj(i + x, j + y) == 0 && abs(img(i + x, j + y) - sum(sum(img .* obj)) / sum(sum(obj))) <= T
                                flag = true;
                                obj(i + x, j + y) = 1;
                            end
                        end
                    end
                end
            end
        end
    end
    new_imgs(:, :, 1) = uint8(img .* obj);
    new_imgs(:, :, 2) = uint8((-obj + 1) * 255);
end
