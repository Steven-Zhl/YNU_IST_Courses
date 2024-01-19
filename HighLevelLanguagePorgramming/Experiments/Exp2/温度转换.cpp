#include <stdio.h> 
int main()
{
    int l;
    int x = 0;
    float k , m;
    printf("请输入温度的数值\n");
	scanf("%d",&l);
	printf("请输入下列选项的代号\n");
	printf("1.摄氏度转华氏度    2.华氏度转摄氏度\n"); 
    scanf("%d",&x);
	if  (x==1)
	    { 
		    k=(l-32.00)*5.00/9.00;
		    printf("华氏度为%.1f",k);
		}
	else
	    {
	    	m=l*9.00/5.00+32.00;
			printf("摄氏度为%.1f",m);
	    };
    return 0;
}
