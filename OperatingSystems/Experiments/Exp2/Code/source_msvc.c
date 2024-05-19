#include <stdio.h>
#include <stdlib.h>
#include <stlbool.h>

typedef struct PCB
{
    int PID;                     // 进程ID
    bool State;                  // 状态（就绪|结束），true表示就绪，false表示结束
    int Total_time;              // 该进程所需的总时间（要求运行时间）
    int CPU_time;                // 该进程已经在CPU中运行的时间（已运行时间）
    struct PCB *Next_PCB = NULL; // 指示下一进程
    int Priority = 0;            // 【仅动态优先级调度使用】优先级
    int Wait_time = 0;           // 【仅最高响应比调度使用】等待时间
} * Proc;

int Proc_num;    // 队列中的进程个数
Proc head, tail; // 两个指针，指向队头和队尾

// 先来先服务
int Init_PCB_FCFS()
{
    int i; // 在循环输入PCB信息时的计数器
    Proc temp, ptr;
    // 输入第一个进程的信息
    printf("Please input the number of processes|请输入进程个数:");
    scanf("%d", &Proc_num);
    printf("There are %d processes, please input PCB info|有%d个进程，请依次输入PCB信息:\n", Proc_num, Proc_num);
    temp = (Proc)malloc(sizeof(struct PCB)); // 进程temp
    printf("----------------Process %2d-----------------\n", 1);
    printf("\tProcess id|PID/进程ID:");
    scanf("%d", &temp->PID);
    printf("\tCPU time required|所需CPU时间:");
    scanf("%d", &temp->Total_time);
    temp->State = true;
    temp->CPU_time = 0; // 就绪，且已运行时间为0
    head = temp;
    tail = temp;
    // 依次输入之后Proc_num-1个进程的信息
    for (i = Proc_num; i > 1; i--)
    {
        ptr = temp; // 先指向上一次的结点
        temp = (Proc)malloc(sizeof(struct PCB));
        printf("----------------Process %2d-----------------\n", Proc_num - i + 2);
        printf("\tProcess id|PID/进程ID:");
        scanf("%d", &temp->PID);
        printf("\tCPU time required|所需CPU时间:");
        scanf("%d", &temp->Total_time);
        temp->State = true;
        temp->CPU_time = 0;
        ptr->Next_PCB = temp;
    }
    tail = temp;
    tail->Next_PCB = head;
    printf("----------------初始化完成-----------------\n");
    return 0;
}

// 动态最高优先级
int Init_PCB_DHPF()
{
    int i; // 在循环输入PCB信息时的计数器
    Proc temp;
    // 输入第一个进程的信息
    printf("Please input the number of processes|请输入进程个数:");
    scanf("%d", &Proc_num);
    printf("There are %d processes, please input PCB info|有%d个进程，请依次输入PCB信息:\n", Proc_num, Proc_num);
    temp = (Proc)malloc(sizeof(struct PCB)); // 进程temp
    printf("----------------Process %2d-----------------\n", 1);
    printf("\tProcess id|PID/进程ID:");
    scanf("%d", &temp->PID);
    printf("\tCPU time required|所需CPU时间:");
    scanf("%d", &temp->Total_time);
    printf("\tProcess priority|进程优先级:");
    scanf("%d", &temp->Priority);
    temp->State = true;
    temp->CPU_time = 0; // 就绪，且已运行时间为0
    head = temp;
    tail = temp;
    // 依次输入之后Proc_num-1个进程的信息
    for (i = Proc_num; i > 1; i--)
    {
        temp = (Proc)malloc(sizeof(struct PCB));
        printf("----------------Process %2d-----------------\n", Proc_num - i + 2);
        printf("\tProcess id|PID/进程ID:");
        scanf("%d", &temp->PID);
        printf("\tCPU time required|所需CPU时间:");
        scanf("%d", &temp->Total_time);
        printf("\tProcess priority|进程优先级:");
        scanf("%d", &temp->Priority);
        temp->State = true;
        temp->CPU_time = 0;
        if (temp->Priority >= head->Priority)
        { // 进程temp优先级最高，将其放在队头
            temp->Next_PCB = head;
            head = temp;
        }
        else
        {
            if (temp->Priority <= tail->Priority)
            { // 进程temp优先级最低，将其放在队尾
                tail->Next_PCB = temp;
                tail = temp;
            }
            else
            { // temp优先级在队列中，则循环找到应该插入队列的地方
                Proc pf = head, pa = head->Next_PCB;
                while (1)
                {
                    if (temp->Priority >= pa->Priority)
                    {
                        pf->Next_PCB = temp;
                        temp->Next_PCB = pa;
                        break;
                    }
                    else
                    {
                        pf = pf->Next_PCB;
                        pa = pa->Next_PCB;
                    }
                }
            }
        }
    }
    tail->Next_PCB = head;
    printf("----------------初始化完成-----------------\n");
    return 0;
}

// 最高响应比（和FCFS的唯一区别就是没有将队尾的NEXT指针指向队首）
int Init_PCB_HRRF()
{
    int i; // 在循环输入PCB信息时的计数器
    Proc temp, ptr;
    // 输入第一个进程的信息
    printf("Please input the number of processes|请输入进程个数:");
    scanf("%d", &Proc_num);
    printf("There are %d processes, please input PCB info|有%d个进程，请依次输入PCB信息:\n", Proc_num, Proc_num);
    temp = (Proc)malloc(sizeof(struct PCB)); // 进程temp
    printf("----------------Process %2d-----------------\n", 1);
    printf("\tProcess id|PID/进程ID:");
    scanf("%d", &temp->PID);
    printf("\tCPU time required|所需CPU时间:");
    scanf("%d", &temp->Total_time);
    temp->State = true;
    temp->CPU_time = 0;
    temp->Wait_time = 0; // 就绪，且已运行时间为0
    head = temp;
    tail = temp;
    // 依次输入之后Proc_num-1个进程的信息
    for (i = Proc_num; i > 1; i--)
    {
        ptr = temp; // 先指向上一次的结点
        temp = (Proc)malloc(sizeof(struct PCB));
        printf("----------------Process %2d-----------------\n", Proc_num - i + 2);
        printf("\tProcess id|PID/进程ID:");
        scanf("%d", &temp->PID);
        printf("\tCPU time required|所需CPU时间:");
        scanf("%d", &temp->Total_time);
        temp->State = true;
        temp->CPU_time = 0;
        temp->Wait_time = 0;
        ptr->Next_PCB = temp;
    }
    tail = temp;
    tail->Next_PCB = NULL;
    printf("----------------初始化完成-----------------\n");
    return 0;
}

// 先来先服务
void Display_FCFS()
{
    int i;
    Proc ptr = head;
    printf(" | PID|进程ID\tCPU_Time|已运行时间\tReq_Time|进程所需总时间 |\n");
    for (i = 0; i < Proc_num; i++)
    {
        printf(" | %-10d\t%-19d\t%-23d |\n", ptr->PID, ptr->CPU_time, ptr->Total_time);
        ptr = ptr->Next_PCB;
    }
}

// 动态最高优先级
void Display_DHPF()
{
    int i;
    Proc ptr = head;
    printf(" | PID|进程ID\tCPU_Time|已运行时间\tReq_Time|进程所需总时间\tPriority|优先级 |\n");
    for (i = 0; i < Proc_num; i++)
    {
        printf(" | %-10d\t%-19d\t%-23d\t%-15d |\n", ptr->PID, ptr->CPU_time, ptr->Total_time, ptr->Priority);
        ptr = ptr->Next_PCB;
    }
}

// 最高响应比
void Display_HRRF()
{
    int i;
    Proc ptr = head;
    printf(" | PID|进程ID\tCPU_Time|已运行时间\tReq_Time|进程所需总时间\tResponse_ratio|响应比 |\n");
    for (i = 0; i < Proc_num; i++)
    {
        printf(" | %-10d\t%-19d\t%-23d\t%-21.4f |\n", ptr->PID, ptr->CPU_time, ptr->Total_time, 1 + ptr->Wait_time / (float)(ptr->Total_time));
        ptr = ptr->Next_PCB;
    }
}

// 先来先服务
void Sched_FCFS()
{
    int round = 1, i;
    Proc temp = tail;
    Proc p = head;
    while (p->Total_time > p->CPU_time)
    {
        printf("\nRound %d, Process %d is running|第%d次轮转，进程%d运行中\n", round, p->PID, round, p->PID);
        p->CPU_time++;
        Display_FCFS();
        if (p->Total_time == p->CPU_time)
        {                     // 进程运行时间已达到要求的时间，表示该进程已执行完毕
            p->State = false; // 置结束标志
            Proc_num--;
            temp->Next_PCB = p->Next_PCB;
            if (p == head)
                head = p->Next_PCB; // 队列后移
            printf("\tProcess %d is finished|进程%d执行完成\n", p->PID, p->PID);
        }
        else
            temp = p;
        p = p->Next_PCB;
        round++;
    }
}

// 动态最高优先级(和FCFS的唯一区别就是多了一个优先级--)
void Sched_DHPF()
{ // 由于在初始化的时候就按照优先级降序进行过排列了，所以在顺序执行的时候优先级降序仍然维持。
    int round = 1, i;
    Proc temp = tail;
    Proc p = head;
    while (p->Total_time > p->CPU_time)
    {
        printf("\nRound %d, Process %d is running|第%d次轮转，进程%d运行中\n", round, p->PID, round, p->PID);
        p->CPU_time++;
        p->Priority--;
        Display_DHPF();
        if (p->Total_time == p->CPU_time)
        {                     // 进程运行时间已达到要求的时间，表示该进程已执行完毕
            p->State = false; // 置结束标志
            Proc_num--;
            temp->Next_PCB = p->Next_PCB;
            if (p == head)
                head = p->Next_PCB; // 队列后移
            printf("\tProcess %d is finished|进程%d执行完成\n", p->PID, p->PID);
        }
        else
            temp = p;
        p = p->Next_PCB;
        round++;
    }
}

// 最高响应比
void Sched_HRRF()
{
    Proc p = head;
    float maxR = 1 + p->Wait_time / (float)(p->Total_time);
    Proc maxP = p;
    while (p->Total_time > p->CPU_time && Proc_num > 0)
    {
        while (p != NULL) // 找出最高响应比的进程
        {
            if (1 + p->Wait_time / (float)(p->Total_time) > maxR)
            {
                maxP = p;
                maxR = 1 + p->Wait_time / (float)(p->Total_time);
            }
            p = p->Next_PCB;
        }
        printf("\nProcess %d is running|进程%d运行中\n", maxP->PID, maxP->PID);
        maxP->CPU_time += 2;
        if (maxP->Total_time <= maxP->CPU_time)
            printf("\tProcess %d is finished|进程%d执行完成\n", maxP->PID, maxP->PID);
        // 其余各进程增加更新时间
        p = head;
        while (p != NULL)
        {
            if (p != maxP)
                p->Wait_time += 2;
            p = p->Next_PCB;
        }
        // 进程完成，将其从队列中清除
        if (maxP->Total_time <= maxP->CPU_time)
        {
            // maxP运行完成
            maxP->State = false;
            if (maxP == head)
            {
                head = head->Next_PCB;
                if (head) // head 非NULL，说明还有进程没做完
                {
                    maxP = head;
                    maxR = 1 + maxP->Wait_time / (float)(maxP->Total_time);
                }
                else // 全部进程已完成
                    break;
            }
            else
            {
                Proc temp = head;
                while (temp != NULL)
                {
                    if (temp->Next_PCB == maxP)
                    {
                        temp->Next_PCB = maxP->Next_PCB;
                        break;
                    }
                    temp = temp->Next_PCB;
                }
            }
            Proc_num--;
        }
        Display_HRRF();
        // 复位
        p = head;
        maxP = p;
        maxR = 1 + p->Wait_time / (float)(p->Total_time);
    }
}

int main()
{
    /*
    // 先来先服务
    Init_PCB_FCFS();
    Display_FCFS();
    Sched_FCFS();
    // 动态最高优先级
    Init_PCB_DHPF();
    Display_DHPF();
    Sched_DHPF();
    */
    // 最高相应比
    Init_PCB_HRRF();
    Display_HRRF();
    Sched_HRRF();
    return 0;
}