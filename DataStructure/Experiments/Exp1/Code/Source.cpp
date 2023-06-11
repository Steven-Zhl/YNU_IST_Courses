#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#define scanf scanf_s

void question1(int num) {
    //num：成绩个数
    double max = 0, min = 100;//记录最大值最小值，这么赋值保证第一次比较的时候可以完成
    int sum = 0;
    double ave;

    double* score = (double*)malloc(num * sizeof(double));//按需求，生成一个长度刚好的数组，用于记录成绩
    for (int i = 0; i < num; i++) {
        printf("请输入第%d个成绩：", i + 1);
        scanf("%lf", &score[i]);
        sum += score[i];
    }
    ave = (double)sum / num;
    for (int i = 0; i < num; i++) {//遍历整个数组，以获得最值而不需要排序
        if (score[i] <= min) {
            min = score[i];
        }
        if (score[i] >= max) {
            max = score[i];
        }
    }
    printf("平均分为%lf，最大值为%lf，最小值为%lf\n", ave, max, min);
}

void question2_loop(int k, int n) {
    //由题意可见，从下标为0的到下标为n的项，共有(n+1)项，在申请空间时需要注意这一点
    int* list = (int*)malloc((n + 1) * sizeof(int));
    for (int i = 0; i <= n; i++) {//按赋值规则赋值
        if (i < k - 1) {
            list[i] = 0;
        }
        else if (i == k - 1) {
            list[i] = 1;
        }
        else if (i > k - 1) {
            list[i] = 0;
            for (int j = 1; j <= k; j++) {
                list[i] += list[i - j];
            }
        }
    }
    printf("%d\n", list[n]);
}

void qusetion2_recursion(int* pointer, int k, int n, int presentOrder) {
    //由题意可见，从下标为0的到下标为n的项，共有(n+1)项，在申请空间时需要注意这一点
    //presentOrder：当前阶数
    if (n<k-1) {
        printf("0\n");
    }
    else if (k-1==n) {
        printf("1\n");
    }
    else {
        if (presentOrder != n) {
            if (presentOrder < k - 1) {
                *pointer = 0;
                qusetion2_recursion((pointer + 1), k, n, (presentOrder + 1));
            }
            if (presentOrder == k - 1) {
                *pointer = 1;
                qusetion2_recursion((pointer + 1), k, n, (presentOrder + 1));
            }
            else if (presentOrder > k - 1) {
                *pointer = 0;
                for (int j = 1; j <= k; j++) {
                    *pointer += *(pointer - j);
                }
                qusetion2_recursion((pointer + 1), k, n, (presentOrder + 1));
            }
        }
        else {
            *pointer = 0;
            for (int j = 1; j <= k; j++) {
                *pointer += *(pointer - j);
            }
            printf("%d\n", *pointer);
            return;
        }
    }
}

void question3_recursion(int n, char a, char b, char c) {
    //先将前(n-1)层移到b，再将第n个移到c，然后将前(n-1)层移到a，多次循环
    if (n == 1) {
        printf("盘子%d：%c---->%c\n", n, a, c);
    }
    else {
        //将前(n - 1)层移到b（通过if部分实现）
        question3_recursion(n - 1, a, c, b);
        //移动第n个到c
        printf("盘子%d：%c---->%c\n", n, a, c);
        //将前(n - 1)层移回a（通过if部分实现）
        question3_recursion(n - 1, b, a, c);
    }
}

void main() {
    printf("问题1：\n");
    int num_1;
    printf("请输入学生人数：");
    scanf("%d", &num_1);
    question1(num_1);
    Sleep(2000);

    printf("\n问题2：\n");
    int k_2, n_2;
    printf("请输入斐波那契数列阶数：");
    scanf("%d", &k_2);
    printf("查看%d阶斐波那契数列的项序列：", k_2);
    scanf("%d", &n_2);
    printf("迭代解法：\n");
    question2_loop(k_2, n_2);
    printf("递归解法：\n");
    int* list = (int*)malloc((n_2 + 1) * sizeof(int));//创建数组
    qusetion2_recursion(list, k_2, n_2, 0);
    Sleep(2000);


    printf("\n问题3：\n");
    int n_3;
    printf("请输入层数n：");
    scanf("%d", &n_3);
    printf("递归解法：\n");
    question3_recursion(n_3, 'a', 'b', 'c');
}