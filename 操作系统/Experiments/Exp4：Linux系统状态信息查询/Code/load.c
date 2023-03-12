#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main()
{
    int i = 1;
    char *p;
    while(1){
        p = (char*) malloc(i * 10 * 1024 * 1024 * sizeof(char));
        memset(p, 1, i * 10 * 1024 * 1024);
        printf("%d\n", i);
        i++;
        sleep(2);
    }
    return 0;
}
