#include <stdio.h>
#include <math.h>
int main()
{
    double pi = 3.1415926535;
    double input1, input2 , z , w;
    float sum;
	scanf("%lf%lf",&input1,&input2);
	z = sin( input1*pi/180 );
	w = cos( input2*pi/180 );
	sum=z+w;
    printf( "sin( %f ) = %f\ncos( %f ) = %f\n", input1 , z , input2 , w);
    printf("sin(%f)+cos(%f)=%f",input1,input2,sum);
    return 0;
}
