#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
void waiting();
void stop();
int wait_mark;
void main(){
	int p1,p2;
	while((p1=fork())==-1);
	if(p1>0){
		while((p2=fork())==-1);
		if(p2>0){
    		printf("parent\n");
    		wait_mark=1;
    		signal(SIGINT,stop);
    		waiting();
    		kill(p1,16);
    		kill(p2,17);
    		wait(0);
    		wait(0);
    		lockf(1,1,0);
    		printf("parent process is killed\n");
    		lockf(1,0,0);
    		exit(0);
	    }else{
    		printf("p2\n");
    		signal(SIGINT, SIG_IGN);
    		wait_mark=1;
    		signal(17,stop);
    		waiting();
    		lockf(1,1,0);
    		printf("child process 2 is killed by parent!\n");
    		lockf(1,0,0);
    		exit(0);
	    }
	}else{
		printf("p1\n");
		signal(SIGINT,SIG_IGN);
		wait_mark=1;
		signal(16,stop);
		waiting();
		lockf(1,1,0);
		printf("child process 1 is killed by parent!\n");
		lockf(1,0,0);
		exit(0);
	}
}

void waiting(){
	while(wait_mark!=0);
}
void stop(){
	wait_mark=0;
}
