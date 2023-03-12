#ifndef _BITREE_H_
#define _BITREE_H_
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <string.h>
#include <math.h>

#define DataType char
#define PREORDER 'A' //通过前序序列构建
#define POSTORDER 'B' //通过后序序列构建

//链二叉树设计
struct BiTreeNode {
	DataType data;
	BiTreeNode* lChild = NULL;
	BiTreeNode* rChild = NULL;

};

//链二叉树的基本操作
struct LinkBiTree {
	BiTreeNode* root = NULL; //根节点(一切的开始)
	int CreateSituation = FALSE; //记录二叉树的构建情况
	int nodeNum = 0; //统计节点数
	int leavesNum = 0; //统计叶子节点数

	//创建链二叉树的函数
	int CreateBiTree(char buildMethod, char* midStr, char* anoStr) {
		//参数分别为：构建二叉树的方式、中序序列、前/后序序列
		//以下步骤为初步检查两个字符串
		if (strlen(anoStr) != strlen(midStr)) {
			printf("您输入的序列长度不一致，无法构建");
			return ERROR;
		}
		if (strlen(anoStr) == 0) {
			printf("该树为空树");
			root->data = 0;
			root->lChild = NULL;
			root->rChild = NULL;
		}
		for (int i = 0; i < strlen(midStr); i++) {
			if (!strchr(anoStr, midStr[i])) {
				printf("您输入的两组序列中，字符不完全一致，无法构建");
				return ERROR;
			}
		}
		nodeNum = strlen(midStr);
		//初步检查完毕，可以构建了
		if (buildMethod == PREORDER) {
			root = PreOrderBuild(anoStr, midStr, 0, nodeNum - 1, 0, nodeNum - 1);
		}
		else if (buildMethod == POSTORDER) {
			root = PostOrderBuild(anoStr, midStr, 0, nodeNum - 1, 0, nodeNum - 1);
		}
		CreateSituation = TRUE;
		return TRUE;
	}

	//通过前序序列和中序序列构建二叉树（实际构建的函数）
	BiTreeNode* PreOrderBuild(char* preStr, char* inStr, int preLEdge, int preREdge, int inLEdge, int inREdge) {
		if (preLEdge > preREdge || inLEdge > inREdge) { return NULL; }
		BiTreeNode* newRoot = (BiTreeNode*)malloc(sizeof(BiTreeNode)); newRoot->data = preStr[preLEdge]; newRoot->lChild = NULL; newRoot->rChild = NULL;
		int lCMidLen = (strchr(inStr, preStr[preLEdge]) - inStr) - inLEdge;//找到当前根节点的左子节点的中序序列的长度
		int rCMidLen = inREdge - (strchr(inStr, preStr[preLEdge]) - inStr);//找到当前根节点的右子节点的中序序列的长度
		preLEdge++;//++表示前序左边界逐步右移，即遍历前序序列，这一步是为构建子树做准备
		//接下来这几行是为了检查是否能构建成二叉树
		DataType lC = preStr[preLEdge], rC = preStr[preREdge - rCMidLen + 1];
		if ((strchr(preStr, lC) - strchr(preStr, rC)) * (strchr(inStr, lC) - strchr(inStr, rC)) < 0) {//小于0说明异号，也就是两者的相对位置不同
			printf("您输入的两个序列不匹配，无法构建成二叉树\n");
			exit(ERROR);
		}
		newRoot->lChild = PreOrderBuild(preStr, inStr, preLEdge, preLEdge + lCMidLen - 1, inLEdge, lCMidLen + inLEdge - 1);
		newRoot->rChild = PreOrderBuild(preStr, inStr, preREdge - rCMidLen + 1, preREdge, inREdge - rCMidLen + 1, inREdge);
		return newRoot;
	}

	//通过后序序列和中序序列构建二叉树（实际构建的函数）
	BiTreeNode* PostOrderBuild(char* postStr, char* inStr, int postLEdge, int postREdge, int inLEdge, int inREdge) {
		if (postLEdge > postREdge || inLEdge > inREdge) { return NULL; }
		BiTreeNode* newRoot = (BiTreeNode*)malloc(sizeof(BiTreeNode)); newRoot->data = postStr[postREdge]; newRoot->lChild = NULL; newRoot->rChild = NULL;
		int lCMidLen = int(strchr(inStr, postStr[postREdge]) - inStr) - inLEdge;//找到当前根节点的左子节点的中序序列的长度
		int rCMidLen = inREdge - int(strchr(inStr, postStr[postREdge]) - inStr);//找到当前根节点的右子节点的中序序列的长度
		//接下来这几行是为了检查所给字符串是否能构建成二叉树
		DataType lC = postStr[postLEdge + lCMidLen - 1], rC = postStr[postREdge - 1];
		if ((strchr(postStr, lC) - strchr(postStr, rC)) * (strchr(inStr, lC) - strchr(inStr, rC)) < 0) {//小于0说明异号，也就是两者的相对位置不同
			printf("您输入的两个序列不匹配，无法构建成二叉树\n");
			exit(ERROR);
		}
		newRoot->lChild = PostOrderBuild(postStr, inStr, postLEdge, postLEdge + lCMidLen - 1, inLEdge, lCMidLen + inLEdge - 1);
		postREdge--;
		newRoot->rChild = PostOrderBuild(postStr, inStr, postLEdge - rCMidLen + 1, postREdge, inREdge - rCMidLen + 1, inREdge);
		return newRoot;
	}

	//前序遍历二叉树
	int PreOrderTraverse(BiTreeNode* root) {
		if (root && CreateSituation) {
			printf("%c", root->data);
			PreOrderTraverse(root->lChild);
			PreOrderTraverse(root->rChild);
		}
		return TRUE;
	}

	//中序遍历二叉树
	int InOrderTraverse(BiTreeNode* root) {
		if (root && CreateSituation) {
			InOrderTraverse(root->lChild);
			printf("%c", root->data);
			InOrderTraverse(root->rChild);
		}
		return TRUE;
	}

	//后序遍历二叉树
	int PostOrderTraverse(BiTreeNode* root) {
		if (root && CreateSituation) {
			PostOrderTraverse(root->lChild);
			PostOrderTraverse(root->rChild);
			printf("%c", root->data);
		}
		return TRUE;
	}

	//返回二叉树深度
	int GetDepth(BiTreeNode* root) {
		int i, j;
		if (!root)
			return 0;
		if (root->lChild)
			i = GetDepth(root->lChild); //左子树深度
		else
			i = 0;
		if (root->rChild)
			j = GetDepth(root->rChild);  //右子树深度
		else
			j = 0;
		return i > j ? i + 1 : j + 1;
	}

	//返回叶节点数
	int LeavesNum(BiTreeNode* root) {//这个只可执行1次，因为它是叶子数++计数，如果该函数需要多次调用的话需要将leavesNum清零再重新开始
		if (root) {
			if (root->lChild == NULL && root->rChild == NULL) { leavesNum++; }
			LeavesNum(root->rChild);
			LeavesNum(root->lChild);
		}
		return leavesNum;
	}
};

//顺序二叉树
struct SqBiTree {
	char* sqTree;//存放顺序二叉树

	void PreOrderBuild(DataType* preStr, DataType* inStr, int preLEdge, int preREdge, int inLEdge, int inREdge, int index) {
		//参数列表依次是：前序序列，中序序列，前序左边界，前序右边界，中序左边界，中序右边界，原数据数组，当前节点的index
		if (preLEdge > preREdge || inLEdge > inREdge) { if (index < strlen(sqTree))sqTree[index] = 0; return; }
		sqTree[index] = preStr[preLEdge];
		int lCMidLen = (strchr(inStr, preStr[preLEdge]) - inStr) - inLEdge;//找到当前根节点的左子节点的中序序列的长度
		int rCMidLen = inREdge - (strchr(inStr, preStr[preLEdge]) - inStr);//找到当前根节点的右子节点的中序序列的长度
		preLEdge++;//++表示前序左边界逐步右移，即遍历前序序列，这一步是为构建子树做准备
		//接下来这几行是为了检查是否能构建成二叉树
		DataType lC = preStr[preLEdge], rC = preStr[preREdge - rCMidLen + 1];
		if ((strchr(preStr, lC) - strchr(preStr, rC)) * (strchr(inStr, lC) - strchr(inStr, rC)) < 0) {//小于0说明异号，也就是两者的相对位置不同
			printf("您输入的两个序列不匹配，无法构建成二叉树\n");
			exit(ERROR);
		}
		PreOrderBuild(preStr, inStr, preLEdge, preLEdge + lCMidLen - 1, inLEdge, lCMidLen + inLEdge - 1, 2 * index);
		PreOrderBuild(preStr, inStr, preREdge - rCMidLen + 1, preREdge, inREdge - rCMidLen + 1, inREdge, 2 * index + 1);
	}

	void FindAncestor(int index1, int index2, int& index, char& val) {
		if (sqTree[index1] == 0 || sqTree[index2] == 0) {
			printf("ERROR\n");
			index = -1; val = 0;
			return;
		}
		while (index1 != index2) {
			index1 > index2 ? index1 /= 2 : index2 /= 2;
		}
		index = index1; val = sqTree[index1];
	}
};
#endif