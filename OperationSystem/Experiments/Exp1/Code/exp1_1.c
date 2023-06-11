# include <stdio.h>
void main()
{
	int p1,p2;
	while((p1=fork())==-1);
	if(p1==0)
		putchar('b');
	else
	{
		while((p2=fork())==-1);
		if(p2==0)
			putchar('c');
		else
			putchar('a');
	}
}
