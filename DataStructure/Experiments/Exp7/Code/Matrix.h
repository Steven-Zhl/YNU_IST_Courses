#ifndef _MATRIX_H_
#define _MATRIX_H_
#include <limits.h>
#include <string.h>
#include<stdlib.h>
#include <queue>
using namespace std;
/*
	邻接矩阵在设计上是最大20*20，但实际不一定会使用这么多，所以需要为不用的部分赋值。
	对于图（无权图），邻接矩阵赋值为0即可；对于网（有权图），邻接矩阵赋值为整型的最大值。
*/
#define INFINITY INT_MAX//最大值
#define MAX_VERTEX_NUM 20//最大顶点个数
#define VRType int //顶点间关系，用int表示
#define VertexType char //数据类型

//图类型标记，有向图，有向网，无向图，无向网
enum GraphKind { DG, DN, UDG, UDN };

//边的集合，为了构建图而创建的一个数据类型
struct Arc {
	VertexType startPoint;
	VertexType endPoint;
	VRType weight = 1;
};

//邻接矩阵类型
typedef struct ArcCell {
	VRType adj;//顶点关系（边或弧），图用1\0表示是否相邻，网为权值
	//InfoType* info;//边或弧的相关信息指针
}ArcCell, AdjMatrix[MAX_VERTEX_NUM][MAX_VERTEX_NUM];

//图类型，一个图包括顶点集合（点集V）、邻接矩阵（边集E）、顶点数、边/弧数、还有图类型标记
struct Mgraph {
	VertexType* vexs = (VertexType*)malloc(MAX_VERTEX_NUM * sizeof(VertexType));//顶点向量
	AdjMatrix arcs;//邻接矩阵
	int vexnum = 0, arcnum = 0;//图的顶点数和边或弧数
	GraphKind kind;//图的类型标志
	bool structState = false;
	bool visited[MAX_VERTEX_NUM] = { false };

	//构建图及邻接矩阵
	void structGraphByMatrix(VertexType* vertex, int vertexNum, Arc* arc, int arcNum, GraphKind type) {

		vexnum = vertexNum; arcnum = arcNum;//更新
		kind = type;//更新
		for (int i = 0; i < MAX_VERTEX_NUM; i++) {
			vexs[i] = i < vexnum ? vertex[i] : 0;
		}
		//更新邻接矩阵
		//1.初始化邻接矩阵
		for (int i = 0; i < MAX_VERTEX_NUM; i++) {
			for (int j = 0; j < MAX_VERTEX_NUM; j++) {
				arcs[i][j].adj = (type == DG || type == UDG) ? 0 : INFINITY;
			}
		}
		//2.根据边集为邻接矩阵赋值
		for (int i = 0; i < arcnum; i++) {
			int row = findIndex(arc[i].startPoint);//例如<vexs[2], vexs[5]>就对应arcs[2][5]，行序为2，列序为5
			int column = findIndex(arc[i].endPoint);
			if (type == UDN || type == UDG) {
				arcs[row][column].adj = type == UDG ? 1 : arc[i].weight;
				arcs[column][row].adj = type == UDG ? 1 : arc[i].weight;
			}
			else {
				arcs[row][column].adj = type == DG ? 1 : arc[i].weight;
			}
		}
		structState = true;//确定已完成构建
	}

	//根据值，查找元素在矩阵中的位置
	int findIndex(VertexType val) {
		for (int i = 0; i < vexnum; i++) {
			if (vexs[i] == val) {
				return i;
			}
		}
		return -1;
	}

	//展示邻接矩阵
	void showArcs() {
		if (structState) {
			for (int i = 0; i < vexnum; i++) {
				for (int j = 0; j < vexnum; j++) {
					printf("%10d ", arcs[i][j].adj);
				}
				printf("\n");
			}
		}
		else {
			printf("您尚未构建矩该图\n");
		}
	}

	//深度优先遍历
	void DFS() {
		memset(visited, false, sizeof(visited));

		for (int i = 0; i < vexnum; i++)
			if (visited[i] == false)
				DFS_Traverse(i);
	}

	//DFS的递归
	void DFS_Traverse(int v) {
		printf("%c", vexs[v]);
		visited[v] = true;
		int adj = FindAdjVertex(v);
		while (adj != -1) {
			if (visited[adj] == false)
				DFS_Traverse(adj);

			adj = FindAdjVertex(v);
		}
	}

	//广度优先遍历
	void BFS() {
		memset(visited, false, sizeof(visited));

		for (int i = 0; i <= vexnum; i++)
			if (visited[i] == false)
				BFS_Traverse(i);
	}

	//BFS的递归函数
	void BFS_Traverse(int v) {

		queue<int> myqueue;
		int adj, temp;

		printf("%c", vexs[v]);
		visited[v] = true;
		myqueue.push(v);

		while (!myqueue.empty()) {    //队列非空表示还有顶点未遍历到    

			temp = myqueue.front();  //获得队列头元素    
			myqueue.pop();         //头元素出对    

			adj = FindAdjVertex(temp);
			while (adj != -1)
			{
				if (visited[adj] == false)
				{
					printf("%c", vexs[adj]);
					visited[adj] = true;
					myqueue.push(adj);   //进对    
				}
				adj = FindAdjVertex(temp);
			}
		}
	}

	//查找该点的邻接点
	int FindAdjVertex(int x) {
		if (kind == UDG) {
			for (int i = 0; i <= vexnum; i++)
				if (arcs[x][i].adj == 1 && visited[i] == false)
					return i;
		}
		return -1;//表示不存在邻接点
	}

	//判断能否填色（本质上就是利用深度优先遍历，按照遍历情况，给当前点的邻接点填上颜色。在遍历过程中一旦出现邻接点颜色和当前颜色相同的情况，即判断不行）
	bool IfCouldAddColor() {
		int color[MAX_VERTEX_NUM];//每个顶点的颜色标记，0记为颜色1，1记为颜色2，-1记为未填色状态
		memset(visited, false, sizeof(visited));
		memset(color, -1, sizeof(color));//记录颜色，同时也起到visited数组的作用
		int satisfy = 1;
		for (int i = 0; i < vexnum; i++)
			if (color[i] == -1)
				addColor(i, color, 0);

		memset(visited, false, sizeof(visited));
		for (int i = 0; i < vexnum; i++)
			if (visited[i] == false)
				satisfy *= checkColor(i, color);

		return satisfy;
	}

	//递归函数:递归地填色
	void addColor(int index, int* arr, int color) {

		arr[index] = color;//给当前点填色
		visited[index] = true;
		int adj = FindAdjVertex(index);//获取到当前点的邻接点
		while (adj != -1) {//存在这个邻接点
			if (visited[adj] == false)//如果邻接点和当前点的颜色不同，则继续递归
				addColor(adj, arr, abs(1 - color));//邻接点换个颜色
			adj = FindAdjVertex(index);
		}
	}

	//检查颜色
	bool checkColor(int index, int* colorArr) {
		queue<int> adjVertex;
		for (int i = 0; i < vexnum; i++) {
			if (arcs[index][i].adj == 1) {
				if (colorArr[index] == colorArr[i] && index != i)
					return false;
			}
		}
		return true;
	}

	//寻路
	bool findArcs(int startVertex, int endVertex) {
		memset(visited, false, sizeof(visited));

		DFS_Traverse(startVertex);
		return (visited[endVertex] == true);
	}

	int Prime(int v)///最小生成树的起点v
	{
		memset(visited, false, sizeof(visited));
		int d[MAX_VERTEX_NUM];//记录从当前树到各的最小权值
		int sum = 0;//最小路径和
		for (int i = 0; i < vexnum; i++)
			d[i] = arcs[v][i].adj;
		d[v] = 0;
		visited[v] = true;//标记遍历过

		for (int i = 1; i < vexnum; i++)///一共n个点，要找n-1条边
		{
			int minn = INFINITY, k=v;//minn是最小权边，k是其对应的index
			for (int j = 0; j < vexnum; j++)///在所有u∈U,w∈V-U的边(u,w)∈E中找到一条权值最小的边
			{
				if (minn > d[j] && visited[j] == false)
				{
					k = j;
					minn = d[j];
				}
			}
			visited[k] = true;///将此点加入最小生成树中
			sum += d[k];
			for (int j = 0; j < vexnum; j++)//更新不在最小生成树的点的边权值，以便找到下一个权值最小的边
			{
				if (visited[j] == false && d[j] > arcs[k][j].adj)
					d[j] = arcs[k][j].adj;
			}
		}
		return sum;///返回生成的最小生成树的权值和
	}

};
#endif