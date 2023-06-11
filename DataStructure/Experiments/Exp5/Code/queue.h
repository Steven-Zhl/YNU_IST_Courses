#ifndef __QUEUE_H__
#define __QUEUE_H__

#include <stdio.h>
#include <stdlib.h>

#define QUEUE_INIT_SIZE 100  //初始容量
#define QUEUE_INCREMENT 10 //增量
#define QElemType char
#define OK 0
#define ERROR -1
#define Status int//用以表示函数的操作状态

//链队列
typedef struct QNode {
	QElemType data = 0;//数据域
	struct QNode* next = NULL;//指针域
}QNode, * QueuePtr;

struct LinkQueue {
	int queueSize = 0;
	QueuePtr front = NULL;//队头指针
	QueuePtr rear = NULL;//队尾指针

	Status InitQueue() {
		QNode* node = (QNode*)malloc(sizeof(QNode));
		node->data = 0;
		node->next = NULL;
		front = node;
		rear = node;
		return OK;
	}

	Status EnQueue(QElemType e) {
		if (queueSize == 0) {
			rear->data = e;
		}
		else {
			QNode* node = (QNode*)malloc(sizeof(QNode));
			node->data = e;
			node->next = NULL;
			rear->next = node;
			rear = rear->next;
		}
		queueSize++;
		return OK;
	}

	Status DeQueue(QElemType& e) {
		if (queueSize != 0) {
			e = front->data;
			QNode* removeNode = front;
			front = front->next;
			free(removeNode);
			queueSize--;
			return OK;
		}
		else {
			printf("队空，无法出队！");
			return ERROR;
		}
	}

	Status ShowQueue() {
		if (queueSize == 0)	printf("当前队为空\n");
		else {
			printf("当前栈内元素为：");
			for (QNode* ptr = front; ptr != rear; ptr = ptr->next) {
				printf("%c->", ptr->data);
			}
			printf("%c", rear->data);
			printf("(由队首至队尾)\n");
		}
		return OK;
	}
};

//循环队列
struct circleQueue {
	int frontIndex;//需要记录front指针的index，以便于结合Count找到队尾
	int lenLimitation = 0;//数组的声明长度，队列的实际容量超出其值则需要扩容
	QElemType* Q;//队列本体
	QElemType* front = NULL;//头指针
	int Count = 0;//计数器

	Status InitQueue() {
		if (Q = (QElemType*)malloc(QUEUE_INIT_SIZE * sizeof(QElemType))) {
			lenLimitation = QUEUE_INIT_SIZE;
			for (int i = 0; i < QUEUE_INIT_SIZE; i++) {//初始化整个队列
				Q[i] = 45;//45是“-”的ASCii
			}
			frontIndex = 0;
			front = &Q[frontIndex];//设置头指针
			return OK;
		}
		else
			return ERROR;
	}

	int EndIndex() {
		if (frontIndex + Count <= lenLimitation) {//队列没有循环
			return frontIndex + Count - 1;
		}
		else {//队列已经循环过了
			return frontIndex + Count - lenLimitation - 1;
		}
		//其实就是return frontIndex + Count <= lenLimitation ? frontIndex + Count - 1 : frontIndex + Count - lenLimitation - 1;
	}

	Status EnQueue(QElemType val) {
		if (Count == 0) {
			Q[frontIndex] = val;
		}
		else if (Count < lenLimitation) {
			Q[EndIndex() == lenLimitation - 1 ? 0 : EndIndex() + 1] = val;
		}
		else {//长度不够了
			Q = (QElemType*)realloc(Q, (QUEUE_INIT_SIZE + QUEUE_INCREMENT) * sizeof(QElemType));
			front = &Q[frontIndex];//重新定位指针
			lenLimitation += QUEUE_INCREMENT;//修改定义量
			EnQueue(val);
		}
		Count++;
		return OK;
	}

	QElemType DeQue(QElemType& e) {
		if (Count != 0) {
			e = Q[frontIndex];
			Q[frontIndex] = 45;//回归未初始化状态
			frontIndex++;
			Count--;
			return OK;
		}
		else {
			printf("队空，无法出队！");
			e = ERROR;
			return ERROR;
		}
	}

	Status ShowQueue() {
		if (Count == 0) {
			printf("当前队列为空\n");
			return ERROR;
		}
		else {
			printf("当前队内元素为：");
			for (int num = 0; num < Count; num++) {
				printf("%c", Q[frontIndex + num < lenLimitation ? frontIndex + num : frontIndex + num - lenLimitation]);
				if (num != Count-1) {
					printf("->");
				}
			}
			printf("(由队首至队尾）\n");
		}
		return OK;
	}
};
#endif