#ifndef __QUES1_H__
#define __QUES1_H__
#include <stdio.h>
#include <stdlib.h>
#define ElemType int //如要修改data的数据类型，则要把ShowList的printf中类型符也进行对应的替换

typedef struct ListNode {
	ElemType val = 0;
	struct ListNode* next = NULL;
}ListNode, * NodePointer;

typedef struct LinkList {//链表
	ListNode headNode;//有头节点的模式
	ListNode* head = &headNode, * tail = &headNode;//节点指针，指向头和尾
	int len = 0;//链表长度

	NodePointer compare(ElemType insertVal, NodePointer comparedNode) {//在return的节点后面插入
		if (insertVal <= comparedNode->val)//比最小的还小，则直接返回头指针即可。
			return head;
		if (insertVal >= tail->val) {//比最大的还大，则直接返回尾指针即可。
			return tail;
		}
		//不比第一个小，不比最后一个大，则在链表内部一定能找到合适的位置。
		if (insertVal > comparedNode->val && insertVal <= comparedNode->next->val) //当前节点比插入值小，但下一个比插入值大
			return comparedNode;
		else
			return compare(insertVal, comparedNode->next);
	}

	void OrderInsert(ElemType val) {
		ListNode* newNode = (ListNode*)malloc(sizeof(ListNode)); newNode->val = val;//为存放新数据而创建一个新node，并初始化 
		NodePointer beforeNode;//指向插入位置之前的节点的指针

		if (len != 0) {//当表不为空时
			beforeNode = compare(val, head);//插入位置之前的Node
			if (beforeNode == tail)tail = newNode;//如果是在表尾插入，则更新tail指针，否则就不用动
		}
		else {
			beforeNode = &headNode;
			tail = newNode;
		}

		newNode->next = beforeNode->next;
		beforeNode->next = newNode;
		len++;
	}

	void OrderInput(ElemType data) {
		OrderInsert(data);
	}
	void OrderMerge(LinkList& La, LinkList& Lb, LinkList& Lc) {
		NodePointer pointer = La.head;
		for (int i = 0; i < La.len; i++) {
			pointer = pointer->next;
			OrderInsert(pointer->val);
		}
		pointer = Lb.head;
		for (int i = 0; i < La.len; i++) {
			pointer = pointer->next;
			OrderInsert(pointer->val);
		}
	}

	void ShowList() {
		NodePointer p = head;
		printf("当前链表为：");
		for (int i = 0; i < len; i++) {
			p = p->next;
			printf("%d", p->val);
			if (i != len - 1) printf(" -> ");
		}
		printf("\n");
	}
}
LinkList;

void ques1_demo()
{
	LinkList la,lb,lc;
	la.OrderInput(4);
	la.OrderInput(21);
	la.OrderInput(13);
	la.ShowList();

	lb.OrderInput(13);
	lb.OrderInput(44);
	lb.OrderInput(3);
	lb.ShowList();

	lc.OrderMerge(la, lb, lc);
	printf("合并后的链表为：\n");
	lc.ShowList();
}
#endif