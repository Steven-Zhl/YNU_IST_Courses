#include <stdio.h>
#include "Matrix.h"
int main() {
	Mgraph map;
	GraphKind type = UDG;//先假定一个无向图

	VertexType vertexs[10] = { 'a','b','c','d','e','f','g','h','i','j' };//假定有10个点

	Arc arcs[12];//假定有12条边
	arcs[0].startPoint = 'a'; arcs[0].endPoint = 'b'; arcs[0].weight = 1;
	arcs[1].startPoint = 'a'; arcs[1].endPoint = 'h'; arcs[1].weight = 1;
	arcs[2].startPoint = 'b'; arcs[2].endPoint = 'c'; arcs[2].weight = 1;
	arcs[3].startPoint = 'b'; arcs[3].endPoint = 'd'; arcs[3].weight = 1;
	arcs[4].startPoint = 'd'; arcs[4].endPoint = 'e'; arcs[4].weight = 1;
	arcs[5].startPoint = 'd'; arcs[5].endPoint = 'f'; arcs[5].weight = 1;
	arcs[6].startPoint = 'd'; arcs[6].endPoint = 'g'; arcs[6].weight = 1;
	arcs[7].startPoint = 'e'; arcs[7].endPoint = 'f'; arcs[7].weight = 1;
	arcs[8].startPoint = 'f'; arcs[8].endPoint = 'g'; arcs[8].weight = 1;
	arcs[9].startPoint = 'h'; arcs[9].endPoint = 'i'; arcs[9].weight = 1;
	arcs[10].startPoint = 'h'; arcs[10].endPoint = 'j'; arcs[10].weight = 1;
	arcs[11].startPoint = 'i'; arcs[11].endPoint = 'j'; arcs[11].weight = 1;
	map.structGraphByMatrix(vertexs, 10, arcs, 12, type);
	map.showArcs();
	bool res = map.IfCouldAddColor();
	return 0;
}