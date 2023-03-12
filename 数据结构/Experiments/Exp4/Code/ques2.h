#ifndef __QUES2_H__
#define __QUES2_H__
#include <stdio.h>
#include <stdlib.h>
#define ParamType double //系数的数据类型

struct equationNode {//多项式每一项
	int power = 0;//阶数
	ParamType param = 0;//系数
	equationNode* next = NULL;
};

struct equation {//多项式
	int nodeNum = 0;//项数
	equationNode* minPow = NULL, * maxPow = NULL;//指向最低阶的节点和最高阶的节点

	void InsertNode(ParamType param, int power) {
		equationNode* newNode = (equationNode*)malloc(sizeof(equationNode)); newNode->param = param; newNode->power = power; newNode->next = NULL;
		if (nodeNum == 0) {//长度为0
			maxPow = newNode;
			minPow = newNode;
		}
		else {//长度不为0
			if (power < minPow->power) {//比较是否比最小值小
				newNode->next = minPow;
				minPow = newNode;
			}
			else if (power > maxPow->power) {//比较是否比最大值大
				maxPow->next = newNode;
				maxPow = newNode;
			}
			else {
				for (equationNode* pointer = minPow; pointer != NULL; pointer = pointer->next) {
					if (pointer->power == power) {
						pointer->param += param;
						nodeNum--;//抵消后面nodeNum++的影响（因为这里实际上是同幂节点的合并）
						break;
					}
					else if (power > pointer->power && power < pointer->next->power) {//遍历寻找合适的位置
						newNode->next = pointer->next;
						pointer->next = newNode;
						break;
					}
				}
			}
		}
		nodeNum++;
	}

	void ShowEquation() {
		equationNode* nodePointer = minPow;
		printf("当前多项式为:\n");
		for (int i = 0; i < nodeNum; i++) {
			if (i != 0)	printf(nodePointer->param > 0 ? " + " : " - ");
			printf("%5.2lf", nodePointer->param > 0 ? nodePointer->param : -(nodePointer->param));
			printf(nodePointer->power == 0 ? "" : "x^%d", nodePointer->power);
			nodePointer = nodePointer->next;
		}
		printf("\n");
	}

	void MergeEquation(equation& Ea, equation& Eb, equation& Ec) {
		equationNode* pointer = Ea.minPow;
		while (pointer != NULL) {//遍历多项式a，向其中添加
			Ec.InsertNode(pointer->param, pointer->power);
			pointer = pointer->next;
		}
		pointer = Eb.minPow;
		while (pointer != NULL) {//遍历多项式b，向其中添加
			Ec.InsertNode(pointer->param, pointer->power);
			pointer = pointer->next;
		}
	}
};
int ques2_demo() {
	equation ea, eb, ec;
	ea.InsertNode(2.13, 4);
	ea.InsertNode(-14.3, 3);
	ea.InsertNode(6.28, 2);
	ea.InsertNode(3.14, 0);
	ea.ShowEquation();

	eb.InsertNode(3.14, 4);
	eb.InsertNode(6.28, 3);
	eb.InsertNode(-14.3, 2);
	eb.InsertNode(2.13, 0);
	eb.ShowEquation();

	ec.MergeEquation(ea, eb, ec);
	ec.ShowEquation();
	return 0;
}
#endif