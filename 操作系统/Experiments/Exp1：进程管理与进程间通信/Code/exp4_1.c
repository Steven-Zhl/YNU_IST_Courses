#include <stdio.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <stdlib.h>

#define SHMKEY 75

int shmid,i;
int *addr;

void CLIENT(){
	int i;
	shmid=shmget(SHMKEY, 1024, 0777|IPC_CREAT);
	addr=shmat(shmid,0,0);
	for(i=9;i>=0;i--){
		while(*addr!=-1);
		printf("(client)sent: %d\n",i);
		*addr=i;
	}
	exit(0);
}
void SERVER(){
	shmid=shmget(SHMKEY, 1024,0777|IPC_CREAT);
	addr=shmat(shmid,0,0);
	do{
		*addr=-1;
		while(*addr==-1);
		printf("(server)received: %d\n",*addr);
	}while(*addr);
	shmctl(shmid,IPC_RMID,0);
	exit(0);
}

int main(){
	while((i=fork())==-1);
	if(!i)SERVER();
	else{
		while((i=fork())==-1);
		if(!i)CLIENT();
		else{
			wait();
			wait();
		}
	}
	return 0;
}
