/*
	题目要求： 
	1、	练习实例程序"Hello world"。	
	2、（1）编程输出"我的信息"，包括姓名、性别、专业名称和课程名称，格式为：
    		姓名：
   			性别：
    		专业名称：
    		课程名称：
		（2）编程计算并输出16.8与27.5两个数的和、差、积、商， 要求输出界面
			和是：                 差是：
			积是：                 商是：
*/ 
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main()
{
    void question1();
    void question2();
    void question3();
    
    question1();
    system("pause");
    
	question2();
    system("pause");
    
	question3();
    system("pause");
    return 0;
}
void question1()
{
    printf("2、\n");
    printf("Hello world!\n");
}
void question2()
{
    printf("选做题（1）\n");
    printf("姓名：张翰林\n性别：男\n专业名称：计算机类\n课程名称：计算机程序设计实验\n");
}
void question3()
{
    float m = 16.8, n = 27.5;
    float a, b, c, d;
    printf("选做题（2）\n");
    a = m + n;
    b = m - n;
    c = m * n;
    d = m / n;
    printf("和是：%3.1f          差是：%3.1f\n积是：%3.0f         商是：%3.1f\n", a, b, c, d);

}
