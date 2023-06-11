#include <stdio.h>
#include <stdlib.h>
#include "BiTree.h"
#include "HuffmanTree.h"
//第一题的3个错误测试用例
void demo1_1() {
	LinkBiTree tree;
	char inStr[6] = "12345";
	char preStr[5] = "1234";
	tree.CreateBiTree(PREORDER, inStr, preStr);
}
void demo1_2() {
	LinkBiTree tree;
	char inStr[5] = "1245";
	char preStr[5] = "1234";
	tree.CreateBiTree(PREORDER, inStr, preStr);
}
void demo1_3() {
	LinkBiTree tree;
	char inStr[5] = "1234";
	char preStr[5] = "4231";
	tree.CreateBiTree(PREORDER, inStr, preStr);
}

void demo2() {
	char inStr[6] = "dbace";
	char preStr[6] = "abdce";
	LinkBiTree tree;
	tree.CreateBiTree(PREORDER, inStr, preStr);
	printf("该二叉树深度为：%d\n", tree.GetDepth(tree.root));
	printf("该二叉树叶子节点个数为：%d\n", tree.LeavesNum(tree.root));
}

void demo3() {
	int arr[] = { 3,9,5,12,6,15 };//测试用例
	HuffmanNode* rootPtr = createTree(arr, 6);  //参数：数据数组、数组长度；返回值：指向哈夫曼树的根节点
	printf("中序遍历结果：");
	InOrderTraverse(rootPtr);
	printf("\n");
	printf("先序遍历结果：");
	PreOrderTraverse(rootPtr);
	printf("\n");
	printf("带权路径长度为：%d\n", calcWeightLength(rootPtr, 0));
}

void demo4() {
	SqBiTree tree;//构建一个顺序二叉树
	char preStr[6] = "abdce";
	char inStr[6] = "dbace";
	tree.sqTree = (char*)malloc(sizeof(char) * 9);//需要计算顺序二叉树数组的长度，为其分配空间
	tree.PreOrderBuild(preStr, inStr, 0, strlen(preStr) - 1, 0, strlen(inStr) - 1, 1);
	int index; char val;
	tree.FindAncestor(2, 3, index, val);//获得祖先index和val
	printf("这两个节点的共同祖先的序列为%d，值为%c", index, val);
	free(tree.sqTree);
}

void demo5() {
	int arr[] = { 8,7,5 };
	HuffmanNode* rootPtr = createTree(arr, 3);
	printf("总花费为：%d\n", calcWeightLength(rootPtr, 0));
}

int main() {
	void demo1_1();
	void demo1_2();
	void demo1_3();
	void demo2();
	void demo3();
	void demo4();
	void demo5();
	demo5();

	return 0;
}
