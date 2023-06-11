#ifndef __STACK_H__
#define __STACK_H__

#include <stdio.h>
#include <stdlib.h>

#define STACK_INIT_SIZE 100  //初始容量
#define STACK_INCREMENT 10 //增量
#define SElemType char //初始化数据元素类型
#define OK 0
#define ERROR -1
#define Status int//用以表示函数的操作状态

// 顺序栈
struct SqStack {
	int stackSize = 0;//已用于存储的容量
	int lenLimitation = 0;//数组的声明长度，栈的实际容量超出其值则需要扩容
	SElemType* S;//栈，本体
	SElemType* base = NULL;//存储基址
	SElemType* top = NULL;//栈顶指针

	Status InitStack() {
		if (S = (SElemType*)malloc(STACK_INIT_SIZE * sizeof(SElemType))) {
			lenLimitation = STACK_INIT_SIZE;
			for (int i = 0; i < STACK_INIT_SIZE; i++) {//为整个栈进行初始赋值
				S[i] = 45;//45是“-”的ASCii
			}
			base = &S[0];
			top = &S[0];
			return OK;
		}
		else
			return ERROR;
	}

	Status Push(SElemType val) {
		if (stackSize < lenLimitation) {//判断栈没满
			if (stackSize == 0) {//栈长度为0时，直接往其中存入，top指针不需要移动
				*top = val;
				stackSize++;
			}
			else {//栈长度不为0，先将top指针后移，然后再存入
				top++;
				*top = val;
				stackSize++;
			}
		}
		else {//栈满
			S = (SElemType*)realloc(S, (STACK_INIT_SIZE + STACK_INCREMENT) * sizeof(SElemType));
			base = &S[0];//重新定位base和top指针
			top = &S[stackSize - 1];
			lenLimitation += STACK_INCREMENT;//修改定义量，即stackSize的上限
			Push(val);
		}
		return OK;
	}

	SElemType Pop(SElemType& e) {
		if (stackSize != 0) {
			stackSize--;
			e = *top--;
			return OK;
		}
		else {
			printf("栈空，无法出栈！");
			e = ERROR;
			return ERROR;
		}
	}

	Status ShowStack() {
		if (stackSize == 0)	printf("当前栈为空\n");
		else {
			printf("当前栈内元素为：");
			for (SElemType* ptr = top; ptr >= base; ptr--) {
				printf("%c", *ptr);
				if (ptr != base) {
					printf("->");
				}
			}
			printf("(由栈顶至栈底)\n");
		}
		return OK;
	}
};
#endif