%% 使用: 在命令行内调用函数Exp1(func)，func是不同功能的名字。要将文件和.m文件放在同一路径下。
%% 每题的demo调用格式如下:
% 1. 读取并显示图像: Exp1("read");
% 2. 显示图像直方图: Exp2("histogram");
% 3. 图像的对比度变换: Exp3("contrast");
% 4. 图像的直方图均衡化: Exp4("equalization");
function Exp1(func)
    img_lena = imread("lena.jpg");
    img_huafen = imread("huafen.tif");

    if func == "read"
        image(img_lena); %展示灰度图
        title("原图");
        axis square;

    elseif func == "histogram"
        bin = input("请输入灰度级数：");
        imhist(img_lena, bin); %划分为128个灰度级
        title("灰度直方图");
        axis square;

    elseif func == "contrast"
        new_img = contrast(img_huafen);
        subplot(1, 2, 1);
        imshow(img_huafen);
        title("原图");
        subplot(1, 2, 2);
        imshow(new_img);
        title("分段线性变换后的图");
        axis square;

    elseif func == "equalization"
        bin = input("请输入灰度级数：");
        new_img = equalizeImg(img_huafen, bin);

        subplot(3, 2, 1)
        imshow(img_huafen);
        title('原图');
        axis square;

        subplot(3, 2, 2)
        imhist(img_huafen);
        title('原图-灰度直方图');
        axis square;

        subplot(3, 2, 3)
        imshow(histeq(img_huafen, bin));
        title('histeq灰度均衡化');
        axis square;

        subplot(3, 2, 4)
        imhist(histeq(img_huafen));
        title('histeq均衡化-灰度直方图');
        axis square;

        subplot(3, 2, 5)
        imshow(new_img);
        title('自制灰度均衡化');
        axis square;

        subplot(3, 2, 6)
        imhist(new_img);
        title('自制灰度均衡化-灰度直方图')
        axis square;
    end

end

%% Ques3: 图像的对比度变换 中 实际计算灰度映射的函数
% Input/输入:
%   grayscale: 原始灰度值，标量
% Output/输出:
%   new_grayscale: 调整后的灰度值，标量
function new_grayscale = adjustGray(grayscale)
    % 将灰度值在100~120之间的像素映射到30~150之间
    if grayscale < 100
        new_grayscale = 0.3 * grayscale;
    elseif grayscale > 120
        new_grayscale = round(106/118 * grayscale + 42.2);
    else
        new_grayscale = round(6 * grayscale - 570);
    end
end

%% Ques3: 图像的对比度变换
% Input/输入:
%   img: 二维矩阵，表示灰度图像
% Output/输出:
%   new_img: 2维灰度矩阵，对比度变换后的结果
function new_img = contrast(img)
    new_img = img;
    for row = 1:length(img)
        for col = 1:length(img)
            new_img(row, col) = adjustGray(img(row, col));
        end
    end
end

%% Ques4: 灰度值均衡化算法
% Input/输入:
%   img: 二维矩阵，表示灰度图像
%   bin: 灰度级数
% Output/输出:
%   new_img: 2维灰度矩阵，直方图均衡化后的结果
function new_img = equalizeImg(img, bin)
    new_img = img;
    [n] = imhist(img, bin); %灰度级的像素个数
    gray2grayRank = [0:1:255; 0:1:255]'; %完成原图的"灰度-灰度级"的对应
    
    for gray = 0:255
        for grayRank = 0:bin - 1
            if gray >= 255 * (grayRank - 1.5) / (bin - 1) && gray < 255 * (grayRank - 0.5) / (bin - 1)
                gray2grayRank(gray + 1, 2) = grayRank;
                break;
            else
                continue;
            end
        end
    end

    counts = n / sum(n); %原始直方图
    cum_counts = cumsum(counts); %累积直方图
    grayRank2grayRank = cum_counts;

    for i = 1:length(counts)
        grayRank2grayRank(i) = round((bin - 1) * cum_counts(i));
    end

    grayRank2grayRank = [[0:1:bin - 1]', grayRank2grayRank]; %灰度级变换，第1列转换为第2列
    grayRank2gray = grayRank2grayRank;

    for grayRank = 0:bin - 1
        grayRank2gray(grayRank + 1, 2) = round(((grayRank) * 256 / bin + (grayRank + 1) * 256 / bin) / 2);
    end

    for row = 1:length(img)
        for col = 1:length(img)
            new_img(row, col) = grayRank2gray(grayRank2grayRank(gray2grayRank(img(row, col), 2), 2), 2);
        end
    end
end
