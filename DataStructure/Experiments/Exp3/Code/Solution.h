#ifndef __SOLUTION_H__
#define __SOLUTION_H__
typedef struct student_message
{
	char *ID = NULL;		 //学号
	double chineseScore = 0; //语文
	double mathScore = 0;	 //数学
	double englishScore = 0; //英语
	double totalScore = 0;	 //总分
	double aveScore = 0;	 //加权平均分
	student_message *next = NULL;
	//计算加权平均分
	void calcAveScore()
	{
		aveScore = chineseScore * 0.3 + mathScore * 0.5 + englishScore * 0.2;
	}
	//计算总分
	void calcTotalScore()
	{
		totalScore = chineseScore + mathScore + englishScore;
	}
	void printStuMes()
	{
		printf("  学号：%s\n", ID);
		printf("  语文成绩：%5.2lf\n", chineseScore);
		printf("  数学成绩：%5.2lf\n", mathScore);
		printf("  英语成绩：%5.2lf\n", englishScore);
		printf("  总成绩：%5.2lf\n", totalScore);
		printf("  加权平均分：%5.2lf\n", aveScore);
	}
} stuNode;

struct listNode
{
	int val;
	listNode *nextNode = NULL;
};

listNode *reverseList(listNode *headNode)
{
	listNode *originNodePointer = headNode; //该指针遍历原链表
	listNode *lastNode = NULL;
	while (originNodePointer->nextNode)
	{
		listNode *newNode = (listNode *)malloc(sizeof(listNode)); //创建一个节点
		newNode->val = originNodePointer->val;					  //新建的节点拷贝原节点值
		newNode->nextNode = lastNode;							  //其nextNode指针域指向上次创建的节点，即头插法
		lastNode = newNode;										  //为下次循环做准备，把这次新建的newNode作为下次的behindNode使用
		originNodePointer = originNodePointer->nextNode;		  //原链表接着遍历
	}
	listNode *newNode = (listNode *)malloc(sizeof(listNode)); //创建一个节点
	newNode->val = originNodePointer->val;					  //新建的节点拷贝原节点值
	newNode->nextNode = lastNode;							  //其nextNode指针域指向上次创建的节点，即头插法
	return newNode;
}
void question4()
{
	listNode *reverseList(listNode * headNode);
	listNode testList[6];
	testList[0].val = 2;
	testList[0].nextNode = &testList[1];
	testList[1].val = 4;
	testList[1].nextNode = &testList[2];
	testList[2].val = 6;
	testList[2].nextNode = &testList[3];
	testList[3].val = 1;
	testList[3].nextNode = &testList[4];
	testList[4].val = 3;
	testList[4].nextNode = &testList[5];
	testList[5].val = 5;
	testList[5].nextNode = NULL;
	printf("测试用例为：2 -> 4 -> 6 -> 1 -> 3 -> 5\n");
	listNode *pointer = reverseList(testList);
	printf("反转结果为：");
	while (pointer)
	{
		printf("%d  ", pointer->val);
		pointer = pointer->nextNode;
	}
	free(pointer);
}
#endif