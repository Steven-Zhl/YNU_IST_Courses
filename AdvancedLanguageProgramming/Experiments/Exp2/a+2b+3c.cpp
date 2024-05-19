#include <stdio.h>
#include <stdlib.h>
int main()
{
	int a,b,c,d,sum;
	scanf("%d%d%d",&a,&b,&c);
	sum=a+2*b+3*c;
	printf("a+2b+3c的值为%d\n",sum);
	system("pause");
	d=a;
	a=b;
	b=d;
	d=c;
	c=b;
	b=d;
	sum=a+2*b+3*c;
	printf("交换之后a+2b+3c的值为%d\n",sum);
	printf("a,b,c的值依次为%d  %d  %d  ",a,b,c);
	
	return 0; 
} 
