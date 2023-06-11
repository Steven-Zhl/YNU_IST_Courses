#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include "solution.h"

stuNode *stu_top = (stuNode *)malloc(sizeof(stuNode));
stuNode *stu_end = NULL;		//指向尾节点，在增添学生时有用
stuNode *stu_pointer = stu_top; //共用的pointer
int stu_num;					//学生人数
int stu_ID_length;				//学号的长度

int main()
{
	//声明函数头
	void menu();		 //操作菜单
	int createStuList(); //创建学生列表
	void iniStuMes();	 //初始化学生信息

	//判断学生列表是否存在，即空间是否分配成功
	if (createStuList())
	{
		printf("申请空间失败，即将退出");
		exit(-1);
	}
	//初始化学生信息
	iniStuMes();
	while (1)
	{
		menu();
	}

	// 以下部分是第四题
	question4();
}
//操作菜单
void menu()
{
	system("cls");
	int choice;
	printf("---------------菜单---------------\n");
	printf("  1. 查看所有学生信息\n");
	printf("  2. 查看单个学生信息\n");
	printf("  3. 追加学生信息\n");
	printf("  4. 删除学生信息\n");
	printf("  5. 学生信息排序\n");
	printf("  6. 退出系统\n");
	printf("  请选择操作：");
	scanf("%d", &choice);
	void printAllStuMes(); //输出所有学生信息
	void printStuMes();	   //输出某个学生信息
	void appendStuMes();   //追加学生信息
	int delStuMes();	   //删除学生信息
	void sortStuMes();	   //按照依据给学生信息升序排列
	switch (choice)
	{
	case 1:
		printAllStuMes();
		break;
	case 2:
		printStuMes();
		break;
	case 3:
		appendStuMes();
		break;
	case 4:
		delStuMes();
		break;
	case 5:
		sortStuMes();
		break;
	case 6:
		system("cls");
		printf("-> 退出系统\n");
		printf("退出成功，感谢使用\n");
		exit(0);
		break;
	default:
		printf("您的输入有误，请重试\n");
		break;
	}
}
//创建起学生链表
int createStuList()
{
	system("cls");
	printf("-> 初始化学生人数\n");
	printf("请输入学生人数：");
	scanf("%d", &stu_num);
	stu_pointer = stu_top; //指向头节点
	for (int i = 0; i < stu_num; i++)
	{
		stuNode *stu_next = (stuNode *)malloc(sizeof(stuNode)); //创建下一个学生
		stu_next->next = NULL;
		stu_pointer->next = stu_next;
		stu_pointer = stu_pointer->next;
	}
	stu_pointer->next = NULL;
	stu_end = stu_pointer;
	return stu_pointer ? 0 : 1;
}
//依据学号，获取目标的前一个学生（为了删除时也能使用）
stuNode *getPreTargetStu(char *targetID)
{
	stu_pointer = stu_top; //指向头节点
	for (int index = 0; index < stu_num; index++)
	{
		if (index == 0 && !strcmp(targetID, stu_pointer->next->ID))
		{ //表示查找的数据恰好为链表中的头节点
			return stu_top;
		}
		else if (!strcmp(targetID, stu_pointer->next->ID))
		{ //查找的数据不是第一个
			return stu_pointer;
		}
		stu_pointer = stu_pointer->next;
	}
	return NULL;
}
//设置学生信息
void setStuMes(stuNode *stu_pointer, int stu_ID_length, int index)
{
	stu_pointer->ID = (char *)malloc((stu_ID_length + 1) * sizeof(char));
	printf("请输入第%d个学生的学号：", index + 1);
	scanf("%s", stu_pointer->ID);
	printf("请输入第%d个学生的语文成绩：", index + 1);
	scanf("%lf", &stu_pointer->chineseScore);
	printf("请输入第%d个学生的数学成绩：", index + 1);
	scanf("%lf", &stu_pointer->mathScore);
	printf("请输入第%d个学生的英语成绩：", index + 1);
	scanf("%lf", &stu_pointer->englishScore);
	fflush(stdin);
	stu_pointer->calcTotalScore(); //计算总分
	stu_pointer->calcAveScore();   //执行计算加权平均分
}
//初始化学生信息
void iniStuMes()
{
	system("cls");
	printf("-> 初始化学生信息\n");
	int index = 0;
	stuNode *stu_pointer = stu_top->next; //指向实际的第一个学生
	printf("请输入学号长度：");
	scanf("%d", &stu_ID_length);
	while (stu_pointer)
	{
		setStuMes(stu_pointer, stu_ID_length, index);
		index++;
		stu_pointer = stu_pointer->next;
	}
	printf("您已初始化完成%d个同学的信息\n", stu_num);
	system("pause");
}
//输出所有学生信息
void printAllStuMes()
{
	system("cls");
	printf("-> 查看所有学生信息\n");
	int index = 0;
	stuNode *stu_pointer = stu_top->next;
	while (stu_pointer)
	{
		printf("\n-------------学生信息%-2d-------------\n", index + 1);
		stu_pointer->printStuMes();
		stu_pointer = stu_pointer->next;
		index++;
	}
	printf("输出完成\n");
	system("pause");
}
//输出某个学生信息
void printStuMes()
{
	system("cls");
	printf("-> 查看单个学生信息\n");
	stuNode *stu_target;
	char *targetID = (char *)malloc((stu_ID_length + 1) * sizeof(char));
	printf("请输入想要查看信息的学生的学号：");
	scanf("%s", targetID);
	stu_target = getPreTargetStu(targetID)->next; //获取到真正目标学生的地址
	if (!stu_target)
	{
		printf("未查找到该学生，即将退出\n");
		system("pause");
		return;
	}
	printf("\n--------------学生信息--------------\n");
	stu_target->printStuMes();
	printf("输出完成\n");
	system("pause");
}
//追加学生信息
void appendStuMes()
{
	system("cls");
	printf("-> 追加学生信息\n");
	int append_num; //要增添的学生数量
	printf("当前已有%d位同学的信息，仍需追加多少同学的信息：", stu_num);
	scanf("%d", &append_num);
	stu_pointer = stu_end; //现在pointer指向了原链表的最后一项。

	for (int i = 0; i < append_num; i++)
	{
		stuNode *stu_next = (stuNode *)malloc(sizeof(stuNode)); //创建一个节点
		stu_next->next = NULL;
		stu_pointer->next = stu_next;
		stu_pointer = stu_pointer->next;
		setStuMes(stu_pointer, stu_ID_length, stu_num + i);
	}
	stu_end = stu_pointer;
	printf("您已完成对%d位同学信息的追加\n", append_num);
	stu_num += append_num; //更新学生人数
	system("pause");
}
//依据学号删除学生信息
int delStuMes()
{
	system("cls");
	printf("-> 删除学生信息\n");
	char *targetID = (char *)malloc((stu_ID_length + 1) * sizeof(char));
	stuNode *stu_preTarget = NULL, *stu_target = NULL;
	printf("请输入被删除的学生的学号：");
	scanf("%s", targetID);
	stu_preTarget = getPreTargetStu(targetID); //获取被删除的前一项
	if (!stu_preTarget)
	{
		printf("未查找到该学生，删除无法执行，即将退出删除\n");
		system("pause");
		return FALSE;
	}
	//执行删除程序
	stu_target = stu_preTarget->next;		//被删除的那一项
	stu_preTarget->next = stu_target->next; //被删除的前一项的指针域指向被删除的后一项

	free(stu_target);
	stu_num--;
	printf("删除成功\n");
	system("pause");
	return TRUE;
}
//学生信息排序
void sortStuMes()
{
	system("cls");
	printf("-> 学生信息排序\n");
	int rank_basis;
	int sort(int choice);
	printf("请选择排序依据：\n");
	printf("1. 学号\n2. 总分\n");
	scanf("%d", &rank_basis);
	printf(sort(rank_basis) ? "排序完成" : "排序过程中出现问题，未完成排序");
	system("pause");
}
//具体的排序方法
int sort(int choice)
{
	int RANK_ID = 1, RANK_SCORE = 2;
	stuNode *stu = (stuNode *)malloc(sizeof(stuNode) * stu_num);
	stu_pointer = stu_top->next;
	for (int i = 0; i < stu_num; i++)
	{
		stu[i].ID = (char *)malloc(sizeof(char) * stu_ID_length); //给字符串分配空间
		//信息拷贝
		strcpy(stu[i].ID, stu_pointer->ID);
		stu[i].chineseScore = stu_pointer->chineseScore;
		stu[i].mathScore = stu_pointer->mathScore;
		stu[i].englishScore = stu_pointer->englishScore;
		stu[i].totalScore = stu_pointer->totalScore;
		stu[i].aveScore = stu_pointer->aveScore;
		stu[i].next = NULL;
		stu_pointer = stu_pointer->next;
	} //此时应该指向了NULL

	int i, j, k, gap; // gap 为步长
	stuNode tmp;
	for (gap = stu_num / 2; gap > 0; gap /= 2)
	{ // 步长初始化为数组长度的一半，每次遍历后步长减半
		for (i = 0; i < gap; ++i)
		{ // 变量 i 为每次分组的第一个元素下标
			for (j = i + gap; j < stu_num; j += gap)
			{				  //对步长为gap的元素进行直插排序，当gap为1时，就是直插排序
				tmp = stu[j]; // 备份stu[j]
				k = j - gap;  // j初始化为i的前一个元素（与i相差gap长度）
				while (k >= 0 && (choice == RANK_ID ? (atoi(stu[k].ID) > atoi(tmp.ID)) : (stu[k].totalScore > tmp.totalScore)))
				{
					stu[k + gap] = stu[k]; // 将在a[i]前且比tmp的值大的元素向后移动一位
					k -= gap;
				}
				stu[k + gap] = tmp;
			}
		}
	}
	stu_pointer = stu_top;
	for (int i = 0; i < stu_num; i++)
	{
		//拷贝信息
		strcpy(stu_pointer->next->ID, stu[i].ID);
		stu_pointer->next->chineseScore = stu[i].chineseScore;
		stu_pointer->next->mathScore = stu[i].mathScore;
		stu_pointer->next->englishScore = stu[i].englishScore;
		stu_pointer->next->totalScore = stu[i].totalScore;
		stu_pointer->next->aveScore = stu[i].aveScore;
		stu_pointer = stu_pointer->next;
	}
	free(stu); //删去整个暂存的数组
	return TRUE;
}