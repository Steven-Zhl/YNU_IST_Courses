#ifndef __SOLUTION_H__
#define __SOLUTION_H__
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

//登录过程中使用
char accountCheck[26];
char codeCheck[26];
int stunum;
//为了让所有的函数也能调用这些数据，使用全局变量
struct students
{
	char name[20];
	char id[30];
	char gender[10];
	char college[20];
	char major[30];
	char note[50];
};
struct students* stu = (struct students*)malloc(stunum * sizeof(struct students));

//初始界面
int surface()
{
	int a;
	puts("┌───────────────────────────────────────────────────────────────────┐");
	puts("│                                                                   │");
	puts("│                  学 生 信 息 管 理 系 统 V 1 . 0                  │");
	puts("│                                                                   │");
	puts("│                             1.登录                                │");
	puts("│                                                                   │");
	puts("│                             2.注册                                │");
	puts("│                                                                   │");
	puts("│                             3.忘记密码                            │");
	puts("│                                                                   │");
	puts("└───────────────────────────────────────────────────────────────────┘");
	puts("欢迎使用！请输入相应操作的代号：");
	scanf("%d", &a);
	getchar();
	return a;
}

//注册账号
int logon()
{
	FILE* check;
	int num = 0;//行数
	char ch;
	char account[26];
	char code[26];
	char accountCompare1[1][26];
	int judge;
	puts("注册账号：");
	puts("请输入您设置的账号：");
	gets(account);
	puts("请输入您设置的密码：");
	gets(code);
	system("cls");
	printf("您设置的账号是：%s\n", account);
	printf("您设置的密码是：%s\n", code);
	puts("是否确认？");
	puts("1.确认正确            2.再次修改");
	scanf("%d", &judge);
	getchar();
	if (judge == 1)
	{
		puts("注册成功！");
		check = fopen("Storage.txt", "a+");//将账号密码写入文件以便于下次登录 
		fseek(check, 0, SEEK_END);
		fprintf(check, "%s\n%s\n", account, code);
		fclose(check);
		return 0;
	}
	else
		return 1;
}

//登录界面
void login()
{
	system("cls");
	printf("统一身份认证");
	printf("\t请先登录：\n");
	printf("账号：__________________________\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b");
	gets(accountCheck);
	system("cls");//清屏，以实现更新界面
	printf("\n账号：%s\n", accountCheck);
	printf("密码：__________________________\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b");
	gets(codeCheck);
	system("cls");
}

//登录检查
int loginCheck()
{
	char accountCompare[26];
	char codeCompare[26];
	char ch;
	int  num;
	FILE* storage;

	//获取行数
	storage = fopen("Storage.txt", "r");
	fseek(storage, 0, SEEK_SET);
	ch = fgetc(storage);
	while (ch != EOF)
	{
		if (ch == '\n')
		{
			num++;
		}
		ch = fgetc(storage);
	}
	fclose(storage);
	num++;

	//此处进行登录检查
	storage = fopen("Storage.txt", "r");
	for (int i = 0, a = 1, b = 1;i < num;i++)
	{
		fscanf(storage, "%s", accountCompare);
		fgetc(storage);
		fscanf(storage, "%s", codeCompare);
		fgetc(storage);
		a = strcmp(accountCheck, accountCompare);
		b = strcmp(codeCheck, codeCompare);
		if (a == 0 && b == 0)
		{
			fclose(storage);
			return 0;
		}
	}
	fclose(storage);
	return 1;
}

//主操作菜单
int menu()
{
	int choice;
	while (true)
	{
		puts("┌─────────────────────────────────────────────────┐");
		puts("│ 学生信息管理系统V1.0                            │");
		puts("│ 1.信息录入                                      │");
		puts("│ 2.修改已有学生信息                              │");
		puts("│ 3.增添学生                                      │");
		puts("│ 4.学生信息查找                                  │");
		puts("│ 5.信息导出                                      │");
		puts("│ 6.手动备份                                      │");
		puts("│ 7.管理员密码修改                                │");
		puts("│ 8.删除学生信息                                  │");
		puts("│ 9.退出程序                                      │");
		puts("└─────────────────────────────────────────────────┘");
		puts("请输入相应的代号进行操作:");
		fflush(stdin);
		scanf("%d", &choice);
		break;
	}
	return choice;
}

//学生信息录入
void stuMesInput(int a, int b)//a代表方式判断值，b表示初始录入的序号。其中a=0表示直接录入，2表示增添学生信息 
{
	int i = 0;
	if (a == 0)//a=0表示从录入开始
	{
		puts("请输入您要录入的学生人数：");
		scanf("%d", &stunum);
	}
	else if (a == 1)//2表示增添学生信息
	{
		i = b;
	}
	for (;i < stunum;i++)
	{
		printf("请输入第%d个同学的姓名：", i + 1);
		scanf("%s", stu[i].name);

		printf("请输入第%d个同学的学号：", i + 1);
		scanf("%s", stu[i].id);

		printf("请输入第%d个同学的性别：", i + 1);
		scanf("%s", stu[i].gender);

		printf("请输入第%d个同学的学院：", i + 1);
		scanf("%s", stu[i].college);

		printf("请输入第%d个同学的专业：", i + 1);
		scanf("%s", stu[i].major);

		printf("备注（若无，则输入“无”）");
		scanf("%s", stu[i].note);
	}
	puts("信息录入完成，即将返回主页");
	system("pause");
	system("cls");
}

//信息查找
int stuMesFind(int judgement)
{
	FILE* dataBase;
	int findIndex, findMethod, num = 0;
	char findContent[20], ch, name[20], id[30], gender[10], college[20], major[30], note[50];
	char* point;

	if (judgement == 1)//0代表从信息查找中来，1代表从删除信息中来
	{
		findMethod = 1;
	}
	else
	{
		puts("请选择查找方式：");
		puts("1.仅在本次输入的内容中查找    2.包含数据库查找");
		scanf("%d", &findMethod);
		if (findMethod != 1 && findMethod != 2)
		{
			puts("操作无效，请重试");
			system("pause");
			system("cls");
			stuMesFind(0);
		}
	} 
	while (true)
	{

		printf("请选择查找索引：\n1.姓名 2.学号 3.学院 4.专业 5.备注\n");
		scanf("%d", &findIndex);
		system("pause");
		system("cls");
		puts("请输入查找内容（不支持模糊查找，请写出对应项的完整名称）");
		scanf("%s", &findContent);
		if (findIndex == 1)
		{
			point = name;//在文件查找里面会用到
			for (int i = 0, judge = strcmp(findContent, stu[i].name);i < stunum;i++)
			{
				if (judge == 0)
				{
					system("cls");
					printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
					if (judgement == 1)
						printf("该学生序号为：%d\n", i);
					system("pause");
					break;
				}
			}
			break;
		}
		else if (findIndex == 2)
		{
			point = id;
			for (int i = 0, judge = strcmp(findContent, stu[i].id);i < stunum;i++)
			{
				if (judge == 0)
				{
					system("cls");
					printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
					if (judgement == 1)
						printf("该学生序号为：%d\n", i);
					system("pause");
					break;
				}
			}
			break;

		}
		else if (findIndex == 3)
		{
			point = college;
			for (int i = 0, judge = strcmp(findContent, stu[i].college);i < stunum;i++)
			{
				if (judge == 0)
				{
					system("cls");
					printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
					if (judgement == 1)
						printf("该学生序号为：%d\n", i);
					system("pause");
					break;
				}
			}
			break;

		}
		else if (findIndex == 4)
		{
			point = major;
			for (int i = 0, judge = strcmp(findContent, stu[i].college);i < stunum;i++)
			{
				if (judge == 0)
				{
					system("cls");
					printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
					if (judgement == 1)
						printf("该学生序号为：%d\n", i);
					system("pause");
					break;
				}
			}
			break;
		}
		else if (findIndex == 5)
		{
			point = note;
			for (int i = 0, judge = strcmp(findContent, stu[i].note);i < stunum;i++)
			{
				if (judge == 0)
				{
					system("cls");
					printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
					if (judgement == 1)
						printf("该学生序号为：%d\n", i);
					system("pause");
					break;
				}
			}
			break;
		}
		else
		{
			puts("操作错误，请重试：");
			system("pause");
			system("cls");
		}

	}
	if (findMethod == 1)
	{
		return 0;
	}
	else if (findMethod == 2)
	{
		dataBase = fopen("student.txt", "r");
		fseek(dataBase, 0, SEEK_SET);
		ch = fgetc(dataBase);
		while (ch != EOF)
		{
			if (ch == '\n')
			{
				num++;
			}
			ch = fgetc(dataBase);
		}
		num++;
		fseek(dataBase, 0, SEEK_SET);
		for (int i = 0, j;i < num;i++)
		{
			fscanf(dataBase, "%s %s %s %s %s %s\n", name, id, gender, college, major, note);
			j = strcmp(point, findContent);
			if (j == 0)
			{
				printf("%s %s %s %s %s %s \n", name, id, gender, college, major, note);
				system("pause");
				system("cls");
			}
		}
		fclose(dataBase);
	}
}

//学生信息增加
int stuAdd()
{
	struct students* stu2;
	int add, stunumOrigin = stunum;
	printf("当前程序中已录入信息的学生数：%d", stunum);
	puts("您需要增添多少位学生的信息？");
	scanf("%d", &add);
	stunum = stunum + add;
	stu2 = (struct students*)realloc(stu, stunum * sizeof(struct students));
	if (stu2 != NULL)
	{
		stu = stu2;
	}
	else
	{
		puts("重申请内存失败");
		exit(0);
	}
	printf("增添请求成功，一共将录入%d位同学的信息,请输入新增同学的信息：", stunum);
	system("pause");
	system("cls");
	return stunumOrigin;
}

//修改已有学生信息
void stuMesEdit()
{
	int i = 0, j, k;
	int findIndex = 0;
	char findContent[20];
	int judge;
	char temporary[50];
	while (true)
	{
		puts("请输入查找内容（不支持模糊查找，请写出对应项的完整名称）");
		scanf("%s", &findContent);
		while (i < stunum)
		{
			judge = strcmp(findContent, stu[i].name);
			if (judge == 0)
			{
				system("cls");
				printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
				printf("学生序号为%d", i);
				system("pause");
				break;
			}
			judge = strcmp(findContent, stu[i].id);
			if (judge == 0)
			{
				system("cls");
				printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
				printf("学生序号为%d", i);
				system("pause");
				break;
			}
			judge = strcmp(findContent, stu[i].gender);
			if (judge == 0)
			{
				system("cls");
				printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
				printf("学生序号为%d", i);
				system("pause");
				break;
			}
			judge = strcmp(findContent, stu[i].college);
			if (judge == 0)
			{
				system("cls");
				printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
				printf("学生序号为%d", i);
				system("pause");
				break;
			}
			judge = strcmp(findContent, stu[i].major);
			if (judge == 0)
			{
				system("cls");
				printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
				printf("学生序号为%d", i);
				system("pause");
				break;
			}
			judge = strcmp(findContent, stu[i].note);
			if (judge == 0)
			{
				system("cls");
				printf("%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
				printf("学生序号为%d", i);
				system("pause");
				break;
			}
			i++;
		}
		break;
	}
	puts("请选择序号：");
	scanf("%d", &j);
	printf("修改前为%s %s %s %s %s %s\n", stu[j].name, stu[j].id, stu[j].gender, stu[j].college, stu[j].major, stu[j].note);
	puts("请选择修改项：1、姓名 2、学号 3、性别 4、学院 5、专业 6、备注");
	scanf("%d", &k);
	puts("请输入修改后的值：");
	scanf("%s", &temporary);
	switch (k)
	{
	case 1:
		strcpy(stu[j].name, temporary);
		break;
	case 2:
		strcpy(stu[j].id, temporary);
		break;
	case 3:
		strcpy(stu[j].gender, temporary);
		break;
	case 4:
		strcpy(stu[j].college, temporary);
		break;
	case 5:
		strcpy(stu[j].major, temporary);
		break;
	case 6:
		strcpy(stu[j].note, temporary);
		break;
	default:
		puts("操作失误，内容未修改");
		break;
	}
	printf("该学生信息当前为%s %s %s %s %s %s\n", stu[j].name, stu[j].id, stu[j].gender, stu[j].college, stu[j].major, stu[j].note);
	system("pause");
}

//学生信息导出
void stuMesOutput()
{
	int i, j;
	char name[40];
	FILE* output;
	output = fopen("student.txt", "r");
	if (output == NULL)//NULL的时候建个新的写进去 
	{
		fclose(output);
		output = fopen("student.txt", "w+");
		fseek(output, 0, SEEK_SET);
		for (i = 0;i < stunum;i++)
		{
			fprintf(output, "%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
		}
		fclose(output);
		puts("信息导出完成，即将返回主页");
		system("pause");
	}
	else
	{
		fclose(output);
		puts("当前已有一份数据，请问是将其覆盖还是另存为一份新的文件？");
		puts("1、覆盖原文件    2、另存为新文件");
		scanf("%d", &j);
		if (j == 1)
		{
			output = fopen("student.txt", "w");
			for (i = 0;i < stunum;i++)
			{
				fprintf(output, "%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
			}
			fclose(output);
			puts("信息导出完成，即将返回主页");
			system("pause");
		}
		else if (j == 2)
		{
			puts("请输入新文件名，注意包含文件后缀：(原文件名：student.txt)");
			scanf("%s", &name);
			output = fopen(name, "w+");
			for (i = 0;i < stunum;i++)
			{
				fprintf(output, "%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
			}
			fclose(output);
			puts("信息导出完成，即将返回主页");
			system("pause");
		}
		else
		{
			puts("操作错误，信息未导出");
			system("pause");
			system("cls");
		}
	}
}

//学生信息备份
void stuMesBackup()
{
	time_t t;
	FILE* backups;
	struct tm* local;
	char totalName[44];
	time(&t);
	local = localtime(&t);
	//asctime(local);//获取到了时间字符串
	if (asctime(local))
	{
		strcpy(totalName, "student_backup_");
		for (int i = 0;i < 24;i++)
			totalName[15 + i] = asctime(local)[i];
		totalName[39] = '.';
		totalName[40] = 't';
		totalName[41] = 'x';
		totalName[42] = 't';
		totalName[43] = '\0';
		totalName[28] = '_';
		totalName[31] = '_';
		backups = fopen(totalName, "w+");
		for (int i = 0;i < stunum;i++)
		{
			fprintf(backups, "%s %s %s %s %s %s\n", stu[i].name, stu[i].id, stu[i].gender, stu[i].college, stu[i].major, stu[i].note);
		}
		fclose(backups);
		puts("信息备份完成，即将返回主页");
		system("pause");
	}
}

//删除学生信息
void deleteMes()
{
	int num, judge;
	while (true)
	{
		stuMesFind(1);
		puts("请选择要删除的学生信息序号：");
		scanf("%d", &num);
		puts("您要删除的信息是：");
		printf("%s %s %s %s %s %s\n", stu[num].name, stu[num].id, stu[num].gender, stu[num].college, stu[num].major, stu[num].note);
		puts("是否确认？");
		puts("1. 确认删除      2.重新选择");
		scanf("%d", &judge);
		if(judge== 1)
		{
			for (int i = num;i < stunum-1;i++)
			{
				strcpy(stu[i].name, stu[i + 1].name);
				strcpy(stu[i].id, stu[i + 1].id);
				strcpy(stu[i].gender, stu[i + 1].gender);
				strcpy(stu[i].college, stu[i + 1].college);
				strcpy(stu[i].major, stu[i + 1].major);
				strcpy(stu[i].note, stu[i + 1].note);
			}
			memset(stu[stunum-1].name,'\0',sizeof(struct students));
			stunum--;
			puts("删除信息成功"); 
			system("pause");
			system("cls");
			break;
		}
		else if(judge== 2)
		{
			puts("取消成功，本次信息未修改");
			system("pause");
			system("cls");
		}
		else
		{
			puts("操作有误，本次信息未修改");
			system("pause");
			system("cls");
		}
	}
}

//修改密码
int adminCodeChange()
{
	FILE* change;
	int judge1, judge2, num = 0, a;
	char ch, code[26], newCode[26], newCodeCheck[26], accountCompare[1][26];
	while (true)
	{
		getchar();
		printf("您当前登录的账号是：%s\n", accountCheck);
		puts("请输入原密码：");
		gets(code);
		judge1 = strcmp(code, codeCheck);
		if (judge1 == 0)
		{
			puts("请输入新密码：");
			gets(newCode);
			system("cls");
			puts("请再输入一次：");
			gets(newCodeCheck);
			judge2 = strcmp(newCode, newCodeCheck);
			if (judge2 == 0)
			{
				puts("修改成功！");

				//获取行数的算法
				change = fopen("Storage.txt", "r");
				ch = fgetc(change);
				while (ch != EOF)
				{
					if (ch == '\n')
					{
						num++;
					}
					ch = fgetc(change);
				}
				fclose(change);
				num++;

				//逐行查找该账号
				change = fopen("Storage.txt", "r+");
				for (int i = 0;i < num;i++)
				{
					if (i % 2 == 0)
					{
						fscanf(change, "%s", accountCompare[0]);
						a = strcmp(accountCheck, accountCompare[0]);
						if (a == 0)//查到了
						{
							fseek(change, 2L, SEEK_CUR);//查到账号之后增加2个偏移量，此时正好在对应的密码开头处 
							fprintf(change, "%s", newCode);
							fclose(change);
							break;
						}
					}
				}
				return 0;
			}
			else
			{
				puts("两次密码不同，请重试");
				system("pause");
				system("cls");
			}
		}
		else
		{
			puts("原密码错误，请重试");
			system("pause");
			system("cls");
		}
	}
}
#endif
