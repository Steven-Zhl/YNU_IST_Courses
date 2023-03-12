#include <stdio.h>
#include "stack.h" //栈
#include "queue.h" //队列
#include "matchBrackets.h" //匹配括号
#include "simulatedStack.h" //模拟入栈出栈
void demo1() {
	SqStack S;
	S.InitStack();//创建空栈
	S.ShowStack();//展示
	S.Push('a');//依次入栈
	S.Push('b');
	S.Push('c');
	S.ShowStack();//展示
	char Sa, Sb, Sc;
	S.Pop(Sa); S.Pop(Sb); S.Pop(Sc);
	printf("%c,%c,%c\n",Sa,Sb,Sc);//依次出栈
	S.ShowStack();//展示
}
void demo2() {
	LinkQueue Q;
	Q.InitQueue();//创建空队
	Q.ShowQueue();//展示
	Q.EnQueue('a');//依次入栈
	Q.EnQueue('b');
	Q.EnQueue('c');
	Q.ShowQueue();//展示
	char Qa, Qb, Qc;
	Q.DeQueue(Qa); Q.DeQueue(Qb); Q.DeQueue(Qc);
	printf("%c,%c,%c\n", Qa, Qb, Qc);//依次出栈
	Q.ShowQueue();//展示
}
void demo3(char a[]) {
	//char a[9] = "(ab)[{}]";
	int res=matchStr(a);
	if (res == OK)
		printf("OK");
	else
		printf("ERROR");
}
void demo4() {
	circleQueue Q;
	Q.InitQueue();
	Q.ShowQueue();
	Q.EnQueue('a');
	Q.EnQueue('b');
	Q.EnQueue('c');
	Q.ShowQueue();
	char Q1, Q2, Q3;
	Q.DeQue(Q1); Q.DeQue(Q2); Q.DeQue(Q3);
	printf("%c,%c,%c\n", Q1, Q2, Q3);//依次出栈
	Q.ShowQueue();//展示
}
void demo5(char a[]) {
	//char a[9] = "SSXXSXSX";
	int res=simulatedStack(a);
	if (res == OK)
		printf("OK");
	else
		printf("ERROR");
}
int main() {
	char a[9] = "SSSXXXXS";
	demo5(a);
}