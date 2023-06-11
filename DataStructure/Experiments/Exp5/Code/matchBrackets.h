#ifndef __MATCHBRACKETS_H__
#define __MATCHBRACKETS_H__

#include "stack.h"

Status matchStr(char* inputStr) {
	SqStack S;
	S.InitStack();
	char* p = inputStr;
	while (*p != '\0') {
		if (*p == '(' || *p == '[' || *p == '{') {//是括号则存进去
			S.Push(*p);
		}
		else if (*p == ')' || *p == ']' || *p == '}') {//出现疑似匹配的括号，则从栈中出一个进行匹配
			char baseElem; S.Pop(baseElem);
			if (!((baseElem == '(' && *p == ')') || (baseElem == '[' && *p == ']') || (baseElem == '{' && *p == '}')))//如果不是能匹配的任一种情况，则返回ERROR
				return ERROR;
		}
		p++;
	}
	if (S.stackSize != 0) return ERROR;//数量不匹配的情况
	return OK;
}

#endif