#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include "solution.h"

int main()
{
	int a, b, start, quit;
	int m = 0, n = 0;
	int command;
	while (true)
	{
		a = surface();//使用a表示在欢迎界面的操作，1表示登录，2表示注册 ,3表示忘记密码 
		if (a == 1)
		{
			break;
		}
		else if (a == 2 || a == 3)
		{
			if (a == 3)
			{
				puts("请重新申请账号");
				system("pause");
				system("cls");
			}
			else;
			system("cls");
			b = logon();//进入注册环节 

			if (b == 1)
			{
				system("cls");
				logon();
			}
			else
			{
				break;
			}
		}
		else
		{
			puts("操作无效，请重试");
			system("pause");
			system("cls");
			break;
		}
	}
	system("cls");
	login();//进行登录 
	while (true)
	{
		if (loginCheck() == 0)
		{
			system("cls");
			puts("欢迎使用");
			fflush(stdin);
			system("pause");
			break;
		}
		else
		{
			puts("账号或密码错误，请重试");
			system("pause");
			system("cls");
			login();
		}
	}
	while (true)
	{
		command = menu();
		//学生信息录入
		if (command == 1)
		{
			puts("学生信息录入");
			system("pause");
			system("cls");
			stuMesInput(0, 0);
		}
		//修改已有学生信息
		else if (command == 2)
		{
			puts("修改已有学生信息");
			system("pause");
			system("cls");
			stuMesEdit();
			system("cls");
		}
		//增添学生
		else if (command == 3)
		{
			puts("增添学生");
			system("pause");
			system("cls");
			start = stuAdd();//用start记录上一次的人数作为下一次录入的起点 
			stuMesInput(1, start);
		}
		//学生信息查找
		else if (command == 4)
		{
			puts("学生信息查找");
			system("pause");
			system("cls");
			stuMesFind(0);
		}
		//信息导出
		else if (command == 5)
		{
			puts("信息导出");
			system("pause");
			system("cls");
			stuMesOutput();
		}
		//学生信息备份
		else if (command == 6)
		{
			puts("学生信息备份");
			system("pause");
			system("cls");
			stuMesBackup();
		}
		//管理员密码修改
		else if (command == 7)
		{
			puts("管理员密码修改");
			system("pause");
			system("cls");
			adminCodeChange();
			puts("您即将退出该程序，请重新登录");
			system("pause");
			system("cls");
			return 0;

		}
		//删除学生信息
		else if (command == 8)
		{
			deleteMes();
		}
		//退出程序 
		else if (command == 9)
		{
			puts("您确定要退出吗？");
			puts("1.退出     2.取消");
			scanf("%d", &quit);
			if (quit == 1)
			{
				return 0;
			}
			else
			{
				system("cls");
			}
		}
		else
		{
			puts("操作错误，请重试！");
			system("pause");
			system("cls");
		}
	}
	fflush(stdin);
	free(stu);
	return 0;
}
