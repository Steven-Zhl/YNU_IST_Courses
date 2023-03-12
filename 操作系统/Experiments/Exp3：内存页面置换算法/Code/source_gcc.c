#include <stdio.h>
#include <stdlib.h>

#define INVALID (-1)
#define TOTAL_PAGE 8 // 页数
#define TOTAL_INSTRUCTION 17
// 页表
typedef struct page_struct {
    int pn;   // 页号
    int pfn;  // 页面号
    int time; // 时间
} page_type;
page_type pl[TOTAL_PAGE];

// free和busy链表
typedef struct page_node {
    int pn;
    int pfn;
    struct page_node *next;
} pfc;

pfc *freepf_head; // 空闲链表头
pfc *busypf_head; // 已用链表头
pfc *busypf_tail; // 已用链表尾

// 相当于每一条指令的页号
int page[TOTAL_INSTRUCTION] = {7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1};;

int diseffect;

// 初始化
void initialize(int total_pf) {
    diseffect = 0;
    freepf_head = NULL;
    // 初始化页表
    for (int i = 0; i < TOTAL_PAGE; i++) {
        pl[i].pn = i;
        pl[i].pfn = INVALID;
        pl[i].time = 0;
    }
    // 初始化空闲页面
    for (int i = 0; i < total_pf; i++) {
        pfc *new_node = (pfc *) malloc(sizeof(pfc));
        new_node->pn = INVALID; // 空闲页面没有页号
        new_node->pfn = i;
        new_node->next = freepf_head;
        freepf_head = new_node;
    }
}

void FIFO(int total_pf) {
    initialize(total_pf);
    diseffect = 0;
    pfc *p;
    busypf_head = busypf_tail = NULL;
    for (int i = 0; i < TOTAL_INSTRUCTION; i++) {
        // 找到需要的页号
        if (pl[page[i]].pfn == INVALID) {// 页面不在内存
            diseffect++;
            if (freepf_head == NULL) {// 没有空闲页框，从busypf表中释放一个页框
                p = busypf_head->next;
                pl[busypf_head->pn].pfn = INVALID;
                freepf_head = busypf_head;
                freepf_head->next = NULL;
                busypf_head = p;
            }
            // 从freepf中取出第一个页框，页面换入该页框
            p = freepf_head->next;
            freepf_head->next = NULL;
            freepf_head->pn = page[i];
            pl[page[i]].pfn = freepf_head->pfn;
            // 将该页框加入busypf中
            if (busypf_tail == NULL) {
                busypf_head = busypf_tail = freepf_head;
            } else {
                busypf_tail->next = freepf_head;
                busypf_tail = freepf_head;
            }
            freepf_head = p;
        }
    }
    printf("FIFO:%.2f%%\n", (1 - (float) diseffect / TOTAL_INSTRUCTION) * 100);
}

void LRU(int total_pf) {
    int min, minj;
    int present_time = 0;
    pfc *p = NULL, *prep = NULL;
    initialize(total_pf);

    for (int i = 0; i < TOTAL_INSTRUCTION; i++) {
        if (pl[page[i]].pfn == INVALID) {
            diseffect++;
            if (freepf_head == NULL) {// 找到time最小的页
                min = 32767;
                for (int j = 0; j < TOTAL_PAGE; j++) {
                    if (min > pl[j].time && pl[j].pfn != INVALID) {
                        min = pl[j].time;
                        minj = j;
                    }
                }
                // 其页框进入freepf
                prep = NULL;
                p = busypf_head;
                while (p != NULL) {
                    if (p->pn == minj) {
                        break;
                    }
                    prep = p;
                    p = p->next;
                }
                // 从busy链表中取出
                if (prep == NULL) {
                    busypf_head = p->next;
                } else {
                    prep->next = p->next;
                }
                // 放入free链表
                freepf_head = p;
                freepf_head->next = NULL;
                pl[minj].pfn = INVALID;
                pl[minj].time = -1;
            }
            // 新页换入freepf中的第一个页框
            p = freepf_head;
            freepf_head = freepf_head->next;
            p->pn = page[i];
            p->next = NULL;
            if (busypf_tail == NULL) {
                busypf_head = p;
            } else {
                busypf_tail->next = p;
            }
            busypf_tail = p;
            pl[page[i]].pfn = p->pfn;
            pl[page[i]].time = present_time;
        } else
            pl[page[i]].time = present_time;
        present_time++;
    }
    printf("LRU:%.2f%%\n", (1 - (float) diseffect / TOTAL_INSTRUCTION) * 100);
}

int main() {
    printf("Query Order|请求顺序:\n");
    for (int i = 0; i < TOTAL_INSTRUCTION; i++)
        printf("%d  ", page[i]);
    printf("\n");
    printf("Three Pages|3页:");
    FIFO(3);
    printf("Three Pages|3页:");
    LRU(3);
    printf("Four Pages| 4页:");
    FIFO(4);
    printf("Four Pages| 4页:");
    LRU(4);
    return 0;
}
