#ifndef __SIMULATEDSTACK_H__
#define __SIMULATEDSTACK_H__

#include "stack.h"
Status simulatedStack(char* inputStr) {
	SqStack S;
	S.InitStack();
	char* p = inputStr;
	while (*p != '\0') {
		if (*p == 'S') {//是'S'则存进去
			S.Push(*p);
		}
		else if (*p == 'X') {
			char val; S.Pop(val);
			if (val == ERROR)return ERROR;
		}
		p++;
	}
	if (S.stackSize != 0) return ERROR;//数量不匹配的情况
	return OK;
}
#endif