%% 使用: 在命令行内调用函数Exp4(func)，func是不同功能的名字。要将文件和.m文件放在同一路径下。
%% 每题的demo调用格式如下:
% 1. 先进行开运算后进行闭运算: Exp4("Ques1");
% 2. 边界提取: Exp4("Ques2");
% 3. 区域填充: Exp4("Ques3");
function Exp4(func)

    if func == "Ques1"
        img = imread("fingerprint.tif");
        se = strel("diamond", 3); % 创建一个菱形结构元
        img_res = Ques1(img, se);
        % 绘图
        subplot(2, 2, 1); imshow(img); title("原图");
        subplot(2, 2, 2); imshow(double(se.Neighborhood)); title("结构元，尺寸：7×7");
        subplot(2, 2, 3); imshow(img_res(:, :, 1)); title("开运算结果");
        for i = 2:size(img_res, 3)
            subplot(2, 2, i + 2); imshow(img_res(:, :, i)); title("第"+num2str(i - 1) + "闭运算结果");
        end

    elseif func == "Ques2"
        img = imread("penny.tif");
        se = strel("diamond", 3); % 创建一个菱形结构元
        img_res = Ques2(img, se);
        subplot(2, 2, 1); imshow(img); title("原图");
        subplot(2, 2, 2); imshow(img_res); title("边界提取");
        subplot(2, 1, 2); imshow(double(se.Neighborhood)); title("结构元，尺寸：7×7");

    elseif func == "Ques3"
        img = im2double(imread("reflections.tif"));
        se = strel("diamond", 3); % 创建一个菱形结构元
        ptr = [59, 54];
        new_img = Ques3(img, ptr, se);
        subplot(2, 2, 1); imshow(img); title("原图");
        subplot(2, 2, 2); imshow(new_img); title("区域填充");
        subplot(2, 1, 2); imshow(double(se.Neighborhood)); title("结构元，尺寸：7×7");
    end

end

%% Ques1: 先进行开运算后进行闭运算
% Input/输入:
%   img: 二维矩阵，表示灰度图像，二值图
%   se: 结构元
% Output/输出:
%   img_new: 3维灰度矩阵，共6层，分别代表开运算结果以及持续进行6次闭运算的结果
function img_new = Ques1(img, se)
    img_new(:, :, 1) = imopen(img, se); % 开运算

    while true
        temp = imclose(img_new(:, :, size(img_new, 3)), se);
        if temp == img_new(:, :, size(img_new, 3)) % 连续两次闭运算结果相同，则退出迭代
            break;
        else
            img_new(:, :, size(img_new, 3) + 1) = temp;
        end
    end
end

%% Ques2: 用结构元对图像进行边界提取
% Input/输入:
%   img: 2维灰度矩阵，表示灰度图像，二值图
%   se: 结构元
% Output/输出:
%   img_new: 2维灰度矩阵，边界提取结果，二值图
function img_new = Ques2(img, se)
    img_erode = imerode(img, se); % 腐蚀操作
    img_new = img - img_erode; % 原图减去腐蚀结果
end

%% Ques3: 用结构元对图像的目标区域进行填充
% Input/输入:
%   img: 2维灰度矩阵，表示灰度图像，二值图
%   ptr: 1×2向量，表示目标区域的起始点
%   se: 结构元
% Output/输出:
%   img_new: 2维灰度矩阵，区域填充结果，二值图
function img_new = Ques3(img, ptr, se)
    img_last = zeros(size(img)); img_last(ptr(1), ptr(2)) = 1; % 初始化
    % 定义交运算和并运算的函数
    and = @(x, y) double(x + y == 2); % ∩:全1为1；全1的话和为2，用这个函数即可表示交运算
    or = @(x, y) double(x + y >= 1); % ∪:有1则1；用这个函数即可表示并运算
    i = 1; %迭代次数

    while 1
        img_new = and(imdilate(img_last, se), ((-img) + 1)); % 先膨胀，再∩运算
        if img_last == img_new % 若前后两次的膨胀结果相同，则迭代结束
            break;
        else
            img_last = img_new;
        end
        i = i + 1; % 计数
    end

    fprintf("迭代次数：%d\n", i);
    img_new = or(img_new, img); % img_new此时只是膨胀区域为1，为保持其他区域不变，要做并运算
end
