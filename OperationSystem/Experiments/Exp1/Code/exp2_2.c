#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>

int pid1,pid2;

void main(){
    int fd[2];
    char outpipe[100],inpipe[100];
    pipe(fd);
    while((pid1=fork())==-1);
    if(pid1==0){
        printf("p1\n");
        lockf(fd[1],1,0);
        sprintf(outpipe,"child 1 process is sending a message!");
        write(fd[1],outpipe,50);
        sleep(1);
        lockf(fd[1],0,0);
        exit(0);
    }else{
        while((pid2=fork())==-1);
        if(pid2==0){
            printf("p2\n");
            lockf(fd[1],1,0);
            sprintf(outpipe,"child 2 process is sending a message!");
            write(fd[1],outpipe,50);
            sleep(1);
            lockf(fd[1],0,0);
            exit(0);
        }else{
            printf("parent\n");
            wait(0);
            read(fd[0],inpipe,50);
            printf("%s\n",inpipe);
            wait(0);
            read(fd[0],inpipe,50);
            printf("%s\n",inpipe);
            exit(0);
        }
    }
}
