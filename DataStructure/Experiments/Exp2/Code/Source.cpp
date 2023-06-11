#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<windows.h>
#include "solution.h"

student* stu = NULL;//学生数组，用来存放学生信息
int stu_num;//学生人数
int stu_ID_length;//学号的长度

int main() {
	//声明函数头
	void menu();//操作菜单
	void iniStuMes();//初始化学生信息
	int createStuList();//创建学生列表

	//判断学生列表是否存在，即空间是否分配成功
	if (createStuList()) {
		printf("申请空间失败，即将退出");
		exit(-1);
	}
	//初始化学生信息
	iniStuMes();
	while (1) {
		menu();
	}
}

//操作菜单
void menu() {
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
	void printAllStuMes();//输出所有学生信息
	void printStuMes();//输出某个学生信息
	void appendStuMes();//追加学生信息
	int delStuMes();//删除学生信息
	void sortStuMes();//按照依据给学生信息升序排列
	switch (choice) {
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

//申请内存，并返回申请结果
int createStuList() {
	system("cls");
	printf("-> 初始化学生人数\n");
	printf("请输入学生人数：");
	scanf("%d", &stu_num);
	stu = (student*)malloc(stu_num * sizeof(student));
	//返回分配情况
	return stu ? 0 : 1;
}

//依据学号，获取学生在数组中的序号
int getStuIndex(char* targetID) {
	int index;
	for (index = 0; index < stu_num; index++) {
		if (!strcmp(targetID, stu[index].ID)) {
			return index;
		}
	}
	return -1;
}

//设置学生信息
void setStuMes(student* stu_pointer, int stu_ID_length, int index) {
	stu_pointer->ID = (char*)malloc((stu_ID_length + 1) * sizeof(char));
	printf("请输入第%d个学生的学号：", index + 1);
	scanf("%s", stu_pointer->ID);
	printf("请输入第%d个学生的语文成绩：", index + 1);
	scanf("%lf", &stu_pointer->chineseScore);
	printf("请输入第%d个学生的数学成绩：", index + 1);
	scanf("%lf", &stu_pointer->mathScore);
	printf("请输入第%d个学生的英语成绩：", index + 1);
	scanf("%lf", &stu_pointer->englishScore);
	fflush(stdin);
	stu_pointer->calcTotalScore();
	stu_pointer->calcAveScore();
}

//初始化学生信息
void iniStuMes() {
	system("cls");
	printf("-> 初始化学生信息\n");
	student* stu_pointer = stu;
	printf("请输入学号长度：");
	scanf("%d", &stu_ID_length);
	fflush(stdin);
	for (int index = 0; index < stu_num; index++, stu_pointer++) {
		setStuMes(stu_pointer, stu_ID_length, index);
	}
	printf("您已初始化完成%d个同学的信息\n", stu_num);
	system("pause");
}

//输出所有学生信息
void printAllStuMes() {
	system("cls");
	printf("-> 查看所有学生信息\n");
	for (int index = 0; index < stu_num; index++) {
		printf("\n-------------学生信息%-2d-------------\n", index + 1);
		stu[index].printStuMes();
	}
	printf("输出完成\n");
	system("pause");
}

//输出学生信息
void printStuMes() {
	system("cls");
	printf("-> 查看单个学生信息\n");
	char* targetID = (char*)malloc((stu_ID_length + 1) * sizeof(char));
	printf("请输入想要查看信息的学生的学号：");
	scanf("%s", targetID);
	int targetIndex = getStuIndex(targetID);//获取被删除的index
	if (targetIndex == -1) {
		printf("未查找到该学生，即将退出\n");
		system("pause");
		return;
	}
	printf("\n--------------学生信息--------------\n");
	stu[targetIndex].printStuMes();
	printf("输出完成\n");
	free(targetID);
	system("pause");
}

//追加学生信息
void appendStuMes() {
	system("cls");
	printf("-> 追加学生信息\n");
	int append_num;
	printf("当前已有%d位同学的信息，仍需追加多少同学的信息：", stu_num);
	scanf("%d", &append_num);
	stu = (student*)realloc(stu, (append_num + stu_num) * sizeof(student));
	if (!stu) {
		printf("追加内存失败，程序即将退出\n");
		exit(-1);
	}

	student* stu_pointer = &stu[stu_num];//现在指向了第一个未初始化的地址
	for (int append = 0; append < append_num; append++, stu_pointer++) {
		setStuMes(stu_pointer, stu_ID_length, stu_num + append);
	}
	printf("您已完成对%d位同学信息的追加\n", append_num);
	stu_num += append_num;//更新学生人数
	system("pause");
}

//依据学号删除学生信息
int delStuMes() {
	system("cls");
	printf("-> 删除学生信息\n");
	char* targetID = (char*)malloc((stu_ID_length + 1) * sizeof(char));
	printf("请输入被删除的学生的学号：");
	scanf("%s", targetID);
	int targetIndex = getStuIndex(targetID);//获取被删除的index
	if (targetIndex == -1) {
		printf("未查找到该学生，删除无法执行，即将退出删除\n");
		system("pause");
		return -1;
	}
	//将其之后的学生信息都向前平移，覆盖掉该学生
	for (int i = targetIndex; i < stu_num - 1; i++) {
		strcpy(stu[i].ID, stu[i + 1].ID);
		stu[i].chineseScore = stu[i + 1].chineseScore;
		stu[i].mathScore = stu[i + 1].mathScore;
		stu[i].englishScore = stu[i + 1].englishScore;
		stu[i].totalScore = stu[i + 1].totalScore;
		stu[i].aveScore = stu[i + 1].aveScore;
	}
	//重分配空间
	stu = (student*)realloc(stu, (stu_num - 1) * sizeof(student));
	stu_num--;
	printf("删除成功\n");
	system("pause");
	free(targetID);
	return 0;
}

//学生信息排序
void sortStuMes() {
	system("cls");
	printf("-> 学生信息排序\n");
	void sort_ID(student * stu, int stu_num);
	void sort_totalScore(student * stu, int stu_num);
	int rank_basis;
	printf("请选择排序依据：\n");
	printf("1. 学号\n2. 总分\n");
	scanf("%d", &rank_basis);
	switch (rank_basis) {
	case 1: {
		sort_ID(stu, stu_num);
		printf("按学号升序排列完成，主菜单中输出所有学生信息即可查看\n");
		break;
	}
	case 2: {
		sort_totalScore(stu, stu_num);
		printf("按总分升序排列完成，主菜单中输出所有学生信息即可查看\n");
		break;
	}
	default: {
		printf("您的输入有误，排序已终止\n");
		break;
	}
	}
	system("pause");
}

//根据学号升序排列
void sort_ID(student* stu, int stu_num)
{
	int i, j, k, gap;// gap 为步长
	student tmp;
	for (gap = stu_num / 2; gap > 0; gap /= 2) {  // 步长初始化为数组长度的一半，每次遍历后步长减半,
		for (i = 0; i < gap; ++i) { // 变量 i 为每次分组的第一个元素下标 
			for (j = i + gap; j < stu_num; j += gap) { //对步长为gap的元素进行直插排序，当gap为1时，就是直插排序
				tmp = stu[j];  // 备份stu[j]
				k = j - gap;  // j初始化为i的前一个元素（与i相差gap长度）
				while (k >= 0 && atoi(stu[k].ID) > atoi(tmp.ID)) {
					stu[k + gap] = stu[k]; // 将在a[i]前且比tmp的值大的元素向后移动一位
					k -= gap;
				}
				stu[k + gap] = tmp;
			}
		}
	}
}

//根据总分升序排列
void sort_totalScore(student* stu, int stu_num) {
	int i, j, k, gap;// gap 为步长
	student tmp;
	for (gap = stu_num / 2; gap > 0; gap /= 2) {  // 步长初始化为数组长度的一半，每次遍历后步长减半,
		for (i = 0; i < gap; ++i) { // 变量 i 为每次分组的第一个元素下标 
			for (j = i + gap; j < stu_num; j += gap) { //对步长为gap的元素进行直插排序，当gap为1时，就是直插排序
				tmp = stu[j];
				k = j - gap;
				while (k >= 0 && stu[k].totalScore > tmp.totalScore) {
					stu[k + gap] = stu[k]; // 将在stu[i]前且比tmp的值大的元素向后移动一位
					k -= gap;
				}
				stu[k + gap] = tmp;
			}
		}
	}
}