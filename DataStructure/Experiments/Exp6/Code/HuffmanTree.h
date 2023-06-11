#ifndef _HUFFMANTREE_H_
#define _HUFFMANTREE_H_
#include<stdio.h>
#include<stdlib.h> 

struct HuffmanNode {
	int data;  //树中节点的值
	HuffmanNode* left;
	HuffmanNode* right;
};

HuffmanNode* createTree(int arr[], int length) {//输入数值节点和数组长度（实际的数值个数）
	HuffmanNode** ptrArr = (HuffmanNode**)malloc(length * sizeof(HuffmanNode*));//存放节点
	HuffmanNode* ptr; HuffmanNode* newRoot = NULL;//指针，分别作为创建时的遍历指针和每层创建的根指针

	for (int i = 0; i < length; i++) {  //依次构建每一个节点，并用数组存放所有节点
		ptr = (HuffmanNode*)malloc(sizeof(HuffmanNode));
		ptr->data = arr[i];
		ptr->left = ptr->right = NULL;
		ptrArr[i] = ptr;
	}

	for (int i = 1; i < length; i++) {  //进行 n-1 次循环建立哈夫曼树  
		//min1Index表示森林中具有最小权值的根结点的下标,min2index为第二小的下标
		int min1Index = -1, min2Index;
		for (int j = 0; j < length; j++) {//先直接取第一下标和第二下标
			if (ptrArr[j] != NULL && min1Index == -1) {
				min1Index = j;
				continue;
			}
			if (ptrArr[j] != NULL) {
				min2Index = j;
				break;
			}
		}
		for (int j = min2Index; j < length; j++) {
			if (ptrArr[j] != NULL) {
				if (ptrArr[j]->data < ptrArr[min1Index]->data) {//依次更新，保证min1Index始终指向最小值，min2Index指向次小值
					min2Index = min1Index;
					min1Index = j;
				}
				else if (ptrArr[j]->data < ptrArr[min2Index]->data) {
					min2Index = j;
				}
			}
		}
		//由最小权值树和次最小权值树建立一棵新树,newRoot为新根
		newRoot = (HuffmanNode*)malloc(sizeof(HuffmanNode));
		newRoot->data = ptrArr[min1Index]->data + ptrArr[min2Index]->data;
		newRoot->left = ptrArr[min1Index];
		newRoot->right = ptrArr[min2Index];

		ptrArr[min1Index] = newRoot; //将指向新树的指针赋给ptrArr指针数组中min1Index
		ptrArr[min2Index] = NULL; //min2Index位置为空
	}
	return newRoot;
}


int calcWeightLength(HuffmanNode*& rootPtr, int len) {
	if (rootPtr == NULL) { //空树返回0
		return 0;
	}
	else {
		if (rootPtr->left == NULL && rootPtr->right == NULL) { //访问到叶子节点
			return rootPtr->data * len;
		}
		else {
			return calcWeightLength(rootPtr->left, len + 1) + calcWeightLength(rootPtr->right, len + 1); //向下递归计算
		}
	}
}

/*
void printHuffmanTreeChildNode(HuffmanTreeNode* node) {
	if (node->left == NULL && node->right == NULL) {
		printf("x=%d是哈夫曼树中的叶子节点", node->data);
		printf("\n\n");
		return;
	}
	if (node->left != NULL) {
		printf("x=%d在哈夫曼树中的左孩子节点是lchild=%d", node->data, node->left->data);
		printf("\n");
	}
	if (node->right != NULL) {
		printf("x=%d在哈夫曼树中的右孩子节点是rchild=%d", node->data, node->right->data);
		printf("\n");
	}
	printf("\n");
}
*/
void InOrderTraverse(HuffmanNode*& rootPtr) {
	if (rootPtr == NULL) {
		return;
	}
	else {
		InOrderTraverse(rootPtr->left);
		printf("%d ", rootPtr->data);
		InOrderTraverse(rootPtr->right);
	}
}

void PreOrderTraverse(HuffmanNode*& rootPtr) {
	if (rootPtr == NULL) {
		return;
	}
	else {
		printf("%d ", rootPtr->data); //依次打印哈夫曼树中各个节点的孩子节点
		PreOrderTraverse(rootPtr->left);
		PreOrderTraverse(rootPtr->right);
	}
}
#endif