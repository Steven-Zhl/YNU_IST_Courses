# 作业

> 书面作业，大概是每次课布置一次，当前的文件是每次的作业汇总。
>
> 当时只保留了源代码，没抄题，但大多数题目是课本原题，留了题号，可以对应参考下。

## 目录

* [作业](#作业)
  * [目录](#目录)
  * [作业1](#作业1)
    * [课本2.1](#课本21)
  * [作业2](#作业2)
    * [课本2.5](#课本25)
    * [课本2.6](#课本26)
  * [作业3](#作业3)
    * [课本3.3](#课本33)
    * [课本3.4](#课本34)
    * [课本3.5](#课本35)
    * [课本3.6](#课本36)
    * [课本3.7](#课本37)
    * [课本3.8](#课本38)
  * [作业4](#作业4)
    * [课本4.5](#课本45)
  * [作业5](#作业5)
    * [课本5.5](#课本55)
    * [课本5.6](#课本56)
    * [课本5.7](#课本57)
    * [课本6.2](#课本62)
    * [编写一个C语言程序，从输入的100个数据中找出最大值](#编写一个c语言程序从输入的100个数据中找出最大值)
  * [作业6](#作业6)
    * [课本6.3](#课本63)
    * [课本6.4](#课本64)
  * [作业7](#作业7)
    * [课本6.4](#课本64-1)
    * [课本7.5](#课本75)
    * [课本8.2](#课本82)
    * [课本8.5](#课本85)
  * [作业8](#作业8)
    * [课本7.3](#课本73)
  * [作业9](#作业9)
    * [课本10.3](#课本103)
    * [课本10.4](#课本104)
    * [课本11.1](#课本111)
    * [课本11.2](#课本112)
    * [课本11.3](#课本113)
    * [课本11.4](#课本114)
  * [作业10](#作业10)
    * [自己编写一个strlen函数，用以计算一个字符串的长度](#自己编写一个strlen函数用以计算一个字符串的长度)
    * [课本9.1](#课本91)
    * [编写一个函数，统计并输出输入的字符串中：各个数字的个数、字母总个数、特殊字符总个数。](#编写一个函数统计并输出输入的字符串中各个数字的个数字母总个数特殊字符总个数)
    * [课本10.2](#课本102)
    * [课本10.3](#课本103-1)
    * [课本10.4](#课本104-1)
  * [作业11](#作业11)
    * [1.](#1)
    * [2.](#2)

## 作业1

### 课本2.1

* 2.1.1

```c
#include <stdio.h>
int main()
{
    printf("姓名：Steven\n街道地址：吴家营街道\n城市：昆明 邮编：650000\n");
    return 0；
}
```

* 2.1.2

```c
#include <stdio.h>
int main()
{
    printf("Computers,computers everywhere\n ");
    printf("as far as I can see\n");
    printf("I really,really like these things,\n");
    printf("Oh joy,Oh joy for me\n");

    return 0；
}
```

* 2.1.3.a
  * 可以使用一条也可以使用多条。
* 2.1.3.b
  * 最少使用一条，使用最少的选择时一行太长且句与句之间没有间隔，可读性低。

```c
printf("Part  No.  Price\nT1267      $6.34\nT1300      $8.92\nT2401      $65.40\nT4482      $36.99\n");
```

* 2.1.3.c

```c
#include <stdio.h>
int main()
{
    printf("3.c\n");
    printf("Part  No.  Price\n");
    printf("T1267      $6.34\n");
    printf("T1300      $8.92\n");
    printf("T2401      $65.40\n");
    printf("T4482      $36.99");
    return 0; 
}
```

## 作业2

### 课本2.5

* 2.5.2

```c
#include<stdio.h>
int main()
{
    float area,radius=2.57;
    area=3.1416*radius*radius;
    printf("该圆的面积为%f",area);
    return 0; 
}
```

* 2.5.6.a

```c
#include<stdio.h>
#include<math.h>
int main()
{
    //1美元=100便士 
    float change,check,paid,dollar; 
    int cent25,cent10,cent5,cent1;
    paid=10.0;
    check=6.07;
    change=(paid-check)*100;//确定零钱中有多少便士 
    dollar=change/100;//确定零钱中的美元数 
    cent25=change/25;
    change=change-cent25*25;
    cent10=change/10;
    change=change-cent10*10;
    cent5=change/5;
    change=change-cent5*5;
    cent1=change/1+1;
    change=change-cent1*1;
    printf("25美分的数量为%d\n1角的数量为%d\n5美分的数量为%d\n1美分的数量为%d\n",cent25,cent10,cent5,cent1);
    printf("%d",change);//此行用于验证是否已经算完，返回值为0时表示已经算完。
    return 0; 
}
```

* 2.5.6.c

```c
#include<stdio.h>
#include<math.h>
int main()
{
    //1美元=100便士 
    float change,check,paid,dollar; 
    int cent25,cent10,cent5,cent1;
    paid=20.0;
    check=12.36;
    change=(paid-check)*100;//确定零钱中有多少便士 
    dollar=change/100;//确定零钱中的美元数 
    cent25=change/25;
    change=change-cent25*25;
    cent10=change/10;
    change=change-cent10*10;
    cent5=change/5;
    change=change-cent5*5;
    cent1=change;
    change=change-cent1*1;
    printf("25美分的数量为%d\n1角的数量为%d\n5美分的数量为%d\n1美分的数量为%d\n",cent25,cent10,cent5,cent1);
    printf("%d",change);//此行用于验证是否已经算完，返回值为0时表示已经算完。
    return 0; 
}
```

### 课本2.6

* 2.6.4

```c
#include <stdio.h>
int main()
{
    long distance,speed,time;
    time=6*6*24*365;//这里少了10^2 
    speed=3;//这里少了10^8 
    distance=time*speed;
    printf("一光年的长度为%d*10^10米",distance);
    return 0;
}
```

* 2.6.7

```c
#include <stdio.h>
int main()
{
    int x1=3,x2=8,y1=7,y2=12;
    float k;
    k=(y2-y1)/(x2-x1);
    printf("%f",k);
    return 0;
}
```

* 2.6.10

```c
#include <stdio.h>
int main()
{
    int n,line1,line2,change;
    scanf("%d",&n);
    line1=n*(n-1)/2;
    printf("%d部电话所需要的线路数为%d\n",n,line1);
    line2=(n+10)*(n-1+10)/2;
    change=line2-line1;
    printf("增加10部新电话时所需的附加线路数为%d",change);
    return 0;
}
```

## 作业3

### 课本3.3

* 3.3.4.a

```c
#include <stdio.h>
int main()
{
    float mile,gallon;
    printf("Enter the miles driven:\n");
    scanf("%f",&mile);
    printf("Enter the gallons of gas used:\n");
    scanf("%f",&gallon);
    printf("The MPG of this car is %.2f",mile/gallon);
    return 0;
}
```

* 3.3.4.b
  * 至少4次，对于两个变量`mile`和`gallon`分别输入整数和小数进行测试，检查结果是否准确。

### 课本3.4

* 3.4.6.a

```c
#include <stdio.h>
int main()
{
    int num1,num2,num3,num4;
    float average;
    printf("Enter a number:\n");
    scanf("%d",&num1);
    printf("Enter a second number:\n");
    scanf("%d",&num2);
    printf("Enter a third number:\n");
    scanf("%d",&num3);
    printf("Enter a fourth number:\n");
    scanf("%d",&num4);
    average=(num1+num2+num3+num4)/4;
    printf("The average of this group of numbers is %f",average);
    return 0;
}
```

* 3.4.6.b

```c
#include <stdio.h>
int main()
{
    int number,sum=0,i=0;
    float ave[3];
    while(i<3)
    {
        printf("Enter a number:\n");
        scanf("%d",&number);
        sum+=number;

        printf("Enter a second number:\n");
        scanf("%d",&number);
        sum+=number;

        printf("Enter a third number:\n");
        scanf("%d",&number);
        sum+=number;

        printf("Enter a fourth number:\n");
        scanf("%d",&number);
        sum+=number;

        ave[i]=sum/4;
        printf("The average of this group of numbers is %f\n",ave[i]);
        sum=0;
        i++;
    }
    printf("%f\n%f\n%f",ave[0],ave[1],ave[2]);
    return 0;
}
```

### 课本3.5

* 3.5.1 求某个圆的周长值

```c
#define pi 3.1416
#include <stdio.h>
int main()
{
    float radius, circum;

    printf("\nEnter a radius");
    scanf("%f", &radius);
    circum = 2.0 * pi * radius;
    printf("\nThe circumference of the circle is%f", circum);

    return 0;
}
```

* 3.5.2 根据利率计算利息

```c
#define prime 0.08
#include <stdio.h>
int main()
{
    float amount,interest;

    printf("\nEnter the amount:");
    scanf("%f", &amount);
   interest = prime * amount;
   printf("\nThe interest earned is %f dollars",interest);

   return 0;
}
```

* 3.5.3 将华氏度转换为摄氏度

```c
#define celsius (5.0/9.0)*(fahren-32)
#include <stdio.h>
int main()
{
    float fahren;

    printf("\nEnter a temperature in degrees Fahrenheit:");
    scanf("%f", &fahren);
    printf("\nThe equivalent Celsius is %f",celsius);

    return 0;
}
```

### 课本3.6

* 3.6.6

```c
#include <stdio.h>
#include <math.h>
int main()
{
    int i;
    int X[7], N[7];
    float R[7],A[7];
    //X：初始存款额（单位：美元）；R：年利率；N：存款年数
    for (i = 0;i < 7;i++)
    {
        printf("(%d)Enter the amount of the initial deposit\n",i+1);//输入初始存款额
        scanf("%d", &X[i]);
        printf("(%d)Enter the your deposit term:\n",i+1);//输入存期，最小单位为年
        scanf("%i", &N[i]);
        printf("(%d)Enter the annual interest rate:\n",i+1);//输入年利率
        scanf("%f", &R[i]);
        if (R[i] < 1)
        {
            R[i] = R[i] * 100;
        }
        else
        {
        }
        A[i] = X[i] * pow(1.0 + R[i] / 100, N[i]);//运算表达式
    }
    printf("每次的总金额为：\n");
    printf("%.2f\n%.2f\n%.2f\n%.2f\n%.2f\n%.2f\n%.2f\n",A[0], A[1],A[2],A[3],A[4],A[5],A[6]);
    return 0;
}
```

* 3.6.8

```c
#include <stdio.h>
#include <math.h>
int main()
{
    float x, y;
    int distance2;
    double distance1;
    printf("请输入向东走的距离\n");
    scanf("%f", &x);
    printf("请输入向北走的距离\n");
    scanf("%f", &y);
    distance1 = sqrt(pow(x,2)+pow(y,2));
    distance2 = (int)(distance1+0.5);
    printf("最短距离为%d（四舍五入后）",distance2);
    return 0;
}
```

### 课本3.7

* 3.7.1
  * 表达式使用变量之前忘记给变量赋值。声明变量时可以赋值，方法是通过赋值语句，或者使用`scanf()`函数交互式地输入值。
* 3.7.2
  * 用一个整型实参调用`sqrt()`函数。这在大多数基于UNIX的编译器上将不会产生编译器错误。在基于Windows的编译器上，将产生一个类似“ambiguous
      call to overloaded function”（重载函数的的声明不明确） 的错误消息。
* 3.7.3
  * `scanf()`函数调用中忘记在变量名的前面使用地址运算符`&`。因为`scanf()`
      函数要求跟随控制字符串的所有参数都是地址，程序员应确保这些地址被正确地传递了。这个编程错误将不会产生编译器错误，但在程序执行时将发生错误。基于UNIX的系统将显示一个类似于“Memory
      fault(coredump)”（内存出错） 的消息，而基于Windows 的系统显示一个类似于”The variable…is being used without being
      defined"（变量未经定义就被使用）的消息。
* 3.7.4
  * 在`scanf()`函数调用中没有包含必须输入的数据值的正确控制字符串。尽管这样做不会产生编译器错误，但当执行这条语句时会导致赋值错误。
* 3.7.5
  * 在传递给`scanf()`函数的控制字符串中包含消息。与`printf()`函数不同的是，`scanf()`
      函数的控制字符串通常只包含控制代码。尽管这样做不会产生编译器错误，但当执行这条语句时会导致赋值错误。
* 3.7.6
  * 用分号终止一个给预处理单元的`#define`命令。到现在为止，你可能会自动用分号终止你的C语言程序中的每行。但是在某些情况下，例如预处理命令，不应该用分号终止。
* 3.7.7
  * 在将一个值赋予符号常量时，将等于号放置在`#define`命令中。
* 3.7.8
  * 将自增和自减运算符用在同一个表达式中多次出现的变量中。这会使外来错误更多地发生，因为C语言中并没有指定表达式中访问操作数的顺序。这会使操作数的访问顺序取决于编译器，也就是取决于编译器如何处理代码。例如，通过下列代码赋予result的值：

  ```c
  i=5;
  result = i + i++;
  ```

  * 根据首先访问的操作数的不同，其结果可以是10或者12。如果编译器首先访问第一个操作数，则这条语句就等价于

  ```c
  result =i +i; /*首先计算结果 */
  i ++;/*然后给i加1*/
  ```

  * 但是，如果编译器首先访问第二个操作数，则语句等价于

  ```c
  i ++;/*首先给i加1*/
  result =i +i; /* 然后计算结果*/
  ```

  * 作为一条通用的原则，应该对在同一表达式中多次出现的变量避免使用自增或者自减运算符，应将表达式拆分成两个，使表达式的顺序能够清楚地表示希望完成的任务。
* 3.7.9
  * 不愿意深入测试程序。不要忘了，在编译之前，程序员都会假定它是正确的，或者如果有错的话会修正它。希望编写程序的人回去老老实实地测试自己的程序，是一件极其困难的事情。作为程序员必须时刻提醒自己，尽管你认为程序是正确的，但是事实往往并不如此。查找自己的程序中的错误是一个冷静的过程，这会使你成为一名真正的程序员。

### 课本3.8

* 3.8.1
  * 算术计算能够使用赋值语句或者数学函数执行，也能够在计算个提供给函数实参值的表达式中执行。
* 3.8.2
  * 赋值符(`=`)是一个运算符，它比所有的数学运算符(`+, -, *, %`)的优先级低。由于赋值是C语言中的一种操作，所以在同一个表达式中一个赋值运算符可以出现多次
* 3.8.3
  * 除了赋值运算符`=`之外，C语言中还提供了`+=`，`-=`，`*=`和`/=`等赋值运算符。
* 3.8.4
  * 自增运算符`++`给变量加1，而自减运算符将变量减1。这两个运算符都能够前置或者后置。在前置操作时，变量在它的值被使用之前加1(或减1)
      ;在后置操作时，变量在它的值被使用之后加1(或减1)。
* 3.8.5
  * C语言中提供了用于计算平方根、对数以及其他数学计算的库函数。使用这些数学函数的每一个程序，都必须包含语句`#include<math.h>`
  ，或者在调用某个数学函数之前对它有一个函数声明。
* 3.8.6
  * 可以将数学函数包含在更大的表达式中。
* 3.8.7
  * `scanf()`函数是用于数据输入的标准库函数，这个函数的参数是一个控制字符串和一个地址列表，它的函数调用一般格式是`scanf("控制字符串", &变量1 ,&变量2.....&变量n);`
  * 控制字符串通常只包含转换控制序列，例如`%d`，且必须包含与地址数量相同的转换控制序列个数。
* 3.8.8
  * 当遇到`scanf()`函数时，程序会临时中止下一条语句的执行，直到已经为这个函数中包含的可变地址数量输入了足够的数据为止。
* 3.8.9
  * 一种好的编程做法是，在调用`scanf()`函数之前显示一条消息，提示用户有关要被输入的数据项的类型和个数。这种消息被称为提示。
* 3.8.10
  * 可以将字段宽度指示符放入转换控制序列中，以明确地指定显示字段的格式。字段宽度指示符包含输出字段的总宽度以及用于浮点型和双精度型数时要显示的小数位数。
* 3.8.11
  * 每一个已编译的C语言程序都会被自动地传递给一个预处理器。在第一列中的用`#`号开始的行，会被当作给预处理器的命令。预处理器命令不以；终止。
* 3.8.12
  * 利用预处理器命令`#define`,可以使表达式与一个标识符等价。这个命令的形式为`#define  标识符  表达式`
  * 在这个命令之后，就可以使用标识符来代替这个表达式。通常而言，会将`#define`命令置于程序的顶部或者`main()`函数的开始处。

## 作业4

### 课本4.5

* 4.5.1.a

```c
#include <stdio.h>
int main()
{
    int month, day;
    printf("Enter a month(use a 1 for Jan, etc.)\n");
    scanf("%d", &month);
    printf("Enter a day of the month\n");
    scanf("%d", &day);
    if ((day > 31 || day < 1) && (month > 12 || month < 1))
    //必须先判断这个，当两者都错的时候才在这里结束，如果把后两个错误语句放在这里有可能提前结束
        printf("Both of the data you input are wrong.");
    else if (month > 12 || month < 1)
        printf("The month you input is wrong.");
    else if (day > 31 || day < 1)
        printf("The day you input is wrong.");
    else
        printf("Both data are right.");
    return 0;
}
```

* 4.5.1.b
  * 如果按照这个程序执行的话，输入小数会将整数部分赋给month，小数点以及小数部分赋给day，导致判断错误。解决方法是将month和day都设为浮点型，然后添加两个变量（judgement1和judgement2）储存这两者除以1的余数，再在外面嵌套一个if判断这两个值是否为0。具体改进如下。

```c
#include <stdio.h>
int main()
{
    float month, day;
    int judgement1,judgement2;
    printf("Enter a month(use a 1 for Jan, etc.)\n");
    scanf("%f", &month);
    printf("Enter a day of the month\n");
    scanf("%f", &day);
    judgement1 = (int)(month * 10) % 10;
    judgement2 = (int)(day * 10) % 10;
    //由于在if的判断条件中只能对整数进行判断，所以这里都扩大10倍，将余数和0比较
    if (judgement1==0&&judgement2==0)
    {
        if ((day > 31 || day < 1) && (month > 12 || month < 1))
        //必须先判断这个，当两者都错的时候才在这里结束，如果把后两个错误语句放在这里有可能提前结束
            printf("Both of the data you input are wrong.");
        else if (month > 12 || month < 1)
            printf("The month you input is wrong.");
        else if (day > 31 || day < 1)
            printf("The day you input is wrong.");
        else
            printf("Both data are right.");
    }
    else
    {
        printf("The data you input include the decimal type data, please check the data and try again.");
    }
    return 0;
}
```

* 4.5.1.c 在确保用户不输入小数的情况下修改1.a的程序如下

```c
#include <stdio.h>
int main()
{
    int month, day;
    printf("Enter a month(use a 1 for Jan, etc.)\n");
    scanf("%d", &month);
    printf("Enter a day of the month\n");
    scanf("%d", &day);
    if ((day > 31 || day < 1) && (month > 12 || month < 1))
    //必须先判断这个，当两者都错的时候才在这里结束，如果把后两个错误语句放在这里有可能提前结束
        printf("Both of the data you input are wrong.");
    else if (month > 12 || month < 1)
        printf("The month you input is wrong.");
    else if (day > 31 || day < 1)
        printf("The day you input is wrong.");
    else//在确保输入的月份和日期不超过最值后再进行细化的判断
    {
        if (month == 2 && day > 28)
            printf("The day of this month is wrong.");
        else if ((month == 4 || month == 6 || month == 9 || month == 11) && day > 30)
            printf("The day of this month is wrong.");
        else printf("Both data are right.");
    }
    return 0;
}
```

* 4.5.3.a

```c
#include <stdio.h>
int main()
{
    int year;
    printf("请输入年份");
    scanf("%d", &year);
    if (year % 4 == 0)
        printf("你输入的是闰年");
    else
        printf("你输入的是平年");
    return 0;
}
```

* 4.5.3.b

```c
#include <stdio.h>
int main()
{
    int day, month, year;
    printf("Enter a year\n");
    scanf("%d", &year);
    printf("Enter a month(use a 1 for Jan, etc.)\n");
    scanf("%d", &month);
    printf("Enter a day of the month\n");
    scanf("%d", &day);
    if ((day > 31 || day < 1) && (month > 12 || month < 1))
    //必须先判断这个，当两者都错的时候才在这里结束，如果把后两个错误语句放在这里有可能提前结束
        printf("Both of the data you input are wrong.");
    else if (month > 12 || month < 1)
        printf("The month you input is wrong.");
    else if (day > 31 || day < 1)
        printf("The day you input is wrong.");
    else//在确保输入的月份和日期不超过最值后再进行细化的判断
    {
        if (year % 4 != 0 && month == 2 && day > 28)//因为闰年与否只影响二月，所以只修改关于二月的判断条件即可
            printf("The day of this month is wrong.");
        else if (year % 4 == 0 && month == 2 && day > 29)
            printf("The day of this month is wrong.");
        else if ((month == 4 || month == 6 || month == 9 || month == 11) && day > 30)
            printf("The day of this month is wrong.");
        else
            printf("Both data are right.");
        return 0;
    }
}
```

* 4.5.4

```c
#include <stdio.h>
int main()
{
    int time,weight;
    float weight1;
    printf("请输入注册时间（单位：年）");
    scanf("%d",&time);
    printf("请输入重量（单位：磅）");
    scanf("%f",&weight1);
    weight = (int)weight1; //可能会出现输入浮点数的情况
    if(time <= 1970)
    {
        if(weight <= 2700)
            printf("重量等级为1，注册费用16.50美元");
        else if(weight >= 2700 && weight <= 3800)
            printf("重量等级为2，注册费用25.50美元");
        else
            printf("重量等级为3，注册费用46.50美元");
    }
    else if(time > 1970 && time < 1980)
    {
        if (weight <= 2700)
            printf("重量等级为4，注册费用27.00美元");
        else if (weight >= 2700 && weight <= 3800)
            printf("重量等级为5，注册费用30.50美元");
        else
            printf("重量等级为6，注册费用52.50美元");
    }
    else
    {
        if (weight <= 3500)
            printf("重量等级为7，注册费用35.50美元");
        else
            printf("重量等级为8，注册费用65.50美元");
    }
    return 0;
}
```

* 4.5.5

```c
#include <stdio.h>
#include <math.h>
int main()
{
    double a, b, c, x1, x2,delta;
    printf("对于二次方程__x^2+__x+__=0，请依次输入各项的系数，以进行计算");
    printf("\n请输入二次项的系数:");
    scanf("%lf", & a);
    printf("\n请输入一次项的系数:");
    scanf("%lf", & b);
    printf("\n请输入常数项:");
    scanf("%lf", & c);
    delta = pow(b, 2) - 4 * a * c;
    x1 = (-b + sqrt(pow(b, 2) - 4 * a * c)) / (2 * a);
    x2 = (-b - sqrt(pow(b, 2) - 4 * a * c)) / (2 * a);
    if (delta < 0)
    {
        printf("该二次方程无实数根");
    }
    else if (delta == 0)
    {
        printf("该二次方程两根相等，x1=x2=%lf", x1);
    }
    else
    {
    printf("该二次方程有两不相等实根，x1=%lf\tx2=%lf", x1, x2);
    }
    return 0;
}
```

## 作业5

### 课本5.5

* 5.5.5

```c
#include <stdio.h>
int main()
{
    int month, day;
    while (1)//循环条件恒成立
    {
        printf("请分别输入月份和日期，用英文逗号隔开\n");
        scanf("%d,%d", &month, &day);
        switch (month)
        {
        case 1:case 3:case 5:case 7:case 8:case 10:case 12:
        {
            if (day <= 31 && day >= 1)
            {
                break;
            }
            else
            {
                printf("日期有误，请重试");
                continue;
            }
        }
        case 4:case 6:case 9:case 11:
        {
            if (day <= 30 && day >= 1)
            {
                break;
            }
            else
            {
                printf("日期有误，请重试");
                continue;
            }
        }
        case 2:
        {
            if (day <= 28 && day >= 1)
            {
                break;
            }
            else
            {
                printf("日期有误，请重试");
                continue;
            }
        }
        default:
        {
            printf("月份有误，请重试\n");
            continue;
        }
        }
        break;
    }
    printf("输入正确，这天是%d月%d日", month, day);
    return 0;
}
```

### 课本5.6

* 5.6.3.a

```c
#include <stdio.h>
int main()
{
    int i, j, a[5][3];
    double ave[5] = { 0,0,0,0,0 };
    for (i = 0;i <= 4;i++)
    {
        for (j = 0;j <= 2;j++)
        {
            printf("请输入第%d名队员的第%d次成绩:", i + 1, j + 1);
            scanf("%d", &a[i][j]);
            ave[i] += a[i][j];
        }
        ave[i] = ave[i] / 3.0;
    }
    for (i = 0;i <= 4;i++)
    {
        printf("第%d个队员的成绩是:%d    %d    %d    ,平均成绩为:%lf\n", i + 1, a[i][0], a[i][1], a[i][2], ave[i]);
    }
    return 0;
}
```

* 5.6.3.b

```c
#include <stdio.h>
int main()
{
    int i, j, a[5][3];
    double ave[5] = { 0,0,0,0,0 }, sum = 0;
    for (i = 0;i <= 4;i++)
    {
        for (j = 0;j <= 2;j++)
        {
            printf("请输入第%d名队员的第%d次成绩:", i + 1, j + 1);
            scanf("%d", &a[i][j]);
            ave[i] += a[i][j];
        }
        sum += ave[i];
        ave[i] = ave[i] / 3;
    }
    for (i = 0;i <= 4;i++)
    {
        printf("第%d个队员的成绩是:%d    %d    %d    ,平均成绩为:%lf\n", i + 1, a[i][0], a[i][1], a[i][2], ave[i]);
    }
    printf("球队平均分为:%lf", sum / 3 );
    return 0;
}
```

### 课本5.7

* 5.7.2

```c
#include <stdio.h>
int main()
{
 double input, sum = 0;
 int i = 0;
 while (1)//循环条件恒成立
 {
  printf("\n请输入本次的分数：");
  scanf("%lf", &input);
  if (input < 0 || input>100 && input != 999)
  {
   printf("\n输入的分数无效，本次不予记录，请重试。");
   continue;
  }
  else if (input == 999)
  {
   printf("\n本次数据不予记录，已跳出循环");
   break;
  }
  else
  {
   sum += input;
   printf("\n本次分数有效，已累加");
   i++;
   continue;
  }
  break;
 }
 printf("\n有效分数的平均值%lf", sum / i);
 return 0;
}
```

### 课本6.2

* 6.2.2.a

```c
double distance(double x1, double x2, double y1, double y2)
{
 double d;
 d = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
 return d;
}
```

* 6.2.2.b

```c
#include <stdio.h>
#include <math.h>
double distance(double x1, double x2, double y1, double y2)
{
 double d;
 d = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
 return d;
}
int main()
{
 double d, x1, x2, y1, y2;
 printf("请依次输入第一个点的坐标（提示：用英文逗号分隔开）\n");
 scanf("%lf,%lf", &x1, &y1);
 printf("\n请依次输入第二个点的坐标（提示：用英文逗号分隔开）\n");
 scanf("%lf,%lf", &x2, &y2);
 d = distance(x1, x2, y1, y2);
 printf("两点间的距离为%lf", d);
 return 0;
}
```

* 6.2.3.a

```c
float tempConvert(float inTemp,char type)
{
 if (type == 'f')
 {
  return ((5.0 / 9.0) * (inTemp - 32.0));
 }
 else 
 {
  return (inTemp * 9.0 / 5.0 + 32.0);
 }
}
```

* 6.2.3.b

```c
#include <stdio.h>
int main()
{
 float tempConvert(float, char);

 int count;
 float inTemp, output;
 char type;

 printf("请选择输入温度类型的代号：\nf、华氏度     c、摄氏度\n");
 scanf("%c", &type);
 printf("\n请输入温度值：");
 scanf("%f", &inTemp);
 output = tempConvert(inTemp, type);
 printf("转换后的温度为%f\n", output);

 return 0;
}
float tempConvert(float inTemp, char type)
{
 if (type == 'f')
 {
  return ((5.0 / 9.0) * (inTemp - 32.0));
 }
 else
 {
  return (inTemp * 9.0 / 5.0 + 32.0);
 }
}
```

### 编写一个C语言程序，从输入的100个数据中找出最大值

```c
#include <stdio.h>
int main()
{
 int i ;
 double a[100], b;
 for (i = 0;i < 100;i++)
 {
  printf("请输入第%d个值：", i + 1);
  scanf("%lf", &a[i]);
 }
 for (i = 0, b = 0;i < 100;i++)
 {
  if (b <= a[i])
  {
   b = a[i];
  }
  else
  {
  }
 }
 printf("最大值为%lf",b);
 return 0;
}
```

## 作业6

### 课本6.3

* 6.3.3.a

```c
#include <stdio.h>
#include <math.h>
#define PI 3.1415927

double volume(double radius, double height)
{
 return PI * pow(radius, 2) * fabs(height);
}
```

* 6.3.3.b

```c
#include <stdio.h>
#include <math.h>
#define PI 3.1415927
double volume(double radius, double height)
{
 return PI * pow(radius, 2) * fabs(height);
}

int main()
{
 double r, h;
 printf("请输入该圆柱体的面半径和高度：");
 scanf("%lf%lf", &r, &h);
 printf("该圆柱体的体积是%lf", volume(r, h));
 return 0;
}
```

* 6.3.6.a

```c
#include <stdio.h>
#include <math.h>
double round(double value, int n)
{
 double value2;
 value2 = (int)(value * pow(10, n)+0.5);
 return value2 / pow(10, n);
}
```

* 6.3.6.b

```c
#define N 2
#include <stdio.h>
#include <math.h>

double round(double value, int n)
{
 double value2;
 value2 = (int)(value * pow(10, n)+0.5);
 return value2 / pow(10, n);
}

int main()
{
 double value;
 printf("请输入存的钱：");
 scanf("%lf", &value);
 printf("您最后得到的利息是%lf", round(value*0.08675, N));
 return 0;
}
```

### 课本6.4

* 6.4.10

```c
#include <stdio.h>

int f(int a, int b)
{
    int c, k;//c为余数
    if (a >= b)
    {
        c = a % b;
        if (c == 0)
            return b;
        else
            return f(b, c);
    }
    else
    {
        k = a;
        a = b;
        b = k;
        c = a % b;
        if (c == 0)
            return b;
        else
            return f(b, c);
    }
}

int main()
{
    int a, b, c;
    printf("输入两个数a b(a≠0且b≠0)\n");
    scanf("%d%d", &a, &b);
    printf("a与b的最大公约数为%d", f(a, b));
    return 0;
}
```

## 作业7

### 课本6.4

* 6.4.2

```c
#include <stdio.h>
#include <math.h>

double dist(double x, double y)
{
 double r;
 r = sqrt(pow(x, 2) + pow(y, 2));
 return r;
}

double angle(double x, double y)
{
 double theta;
 theta = atan(y / x);
 return theta;
}

int main()
{
 double x, y, d, theta;
 printf("请输入该点的直角坐标系横坐标：");
 scanf("%lf", &x);
 printf("请输入该点的直角坐标系纵坐标：");
 scanf("%lf", &y);
 d = dist(x, y);
 theta = angle(x, y);
 printf("该点的极坐标为(%lf,%lf)", d, theta);
 return 0;
}
```

### 课本7.5

* 7.5.1.a 递归写法

```c
#include <stdio.h>

int fib(int n)
{
 if (n == 1)
  return 0;
 else if (n == 2)
  return 1;
 else
  return fib(n - 1)+fib(n - 2);
}

int main()
{
 int n, i = 0;
 printf("请输入要输出数列的第多少项：");
 scanf("%d", &n);
 printf("fibonacci数列的第%d项是：%d\n", n, fib(n));
 return 0;
}
```

* 7.5.1.b 非递归写法

```c
#include <stdio.h>

int fib(int n)
{
 int a1=0,a2=1,sum,i;
 if (n == 1)
  return a1;
 else if (n == 2)
  return a2;
 else
 {
  for (i = 2;i < n;i++)
  {
   sum = a1 + a2;
   a1 = a2;
   a2 = sum;
  }
  return a2;
 }
}

int main()
{
 int n, i = 0;
 printf("请输入要输出数列的第多少项：");
 scanf("%d", &n);
 printf("fibonacci数列的第%d项是：%d\n", n, fib(n));
 return 0;
}
```

### 课本8.2

* 8.2.4

```c
#include <stdio.h>
int main()
{
 int i;
 float max, min, rates[9] = { 18.24,25.63,5.94,33.92,3.71,32.84,35.93,18.24,6.92 };
 for (i = 0, max = 0, min = 999;i < 9;i++)
 {
  if (max < rates[i])
  {
   max = rates[i];
  }
  else
  {
  }
  if (min > rates[i])
  {
   min = rates[i];
  }
  else
  {
  }
 }
 printf("这组数中最大值为%.2f，最小值为%.2f", max, min);
}
```

### 课本8.5

* 8.5.3

```c
#include <stdio.h>

int main()
{
 int first[2][3] = { { 16,18,23 },{54, 91, 11} };
 int second[2][3] = { {24, 52, 77}, { 16,19,59 } };
 int sum[2][3], i, j;
 printf("first和second的和是：\n");
 for (i = 0;i < 2;i++)
 {
  for (j = 0;j < 3;j++)
  {
   sum[i][j] = first[i][j] + second[i][j];
   printf("%-4d", sum[i][j]);
   if (j == 2)
   {
    printf("\n");
   }
   else
   {
    continue;
   }
  }
 }
 return 0;
}
```

## 作业8

### 课本7.3

* 7.3.6.a

```c
void date(long input, int* year, int* month, int* day)
{
 *year = (int)(input/ 10000);
 *month = (int)((input - *year * 10000) / 100);
 *day = (int)(input - *year * 10000 - *month * 100);
}
```

* 7.3.6.b

```c
#include <stdio.h>

int main()
{
 void date(long, int*, int*, int*);
 long in=20201209;
 int year, month,day;
 date(in, &year, &month, &day);
 printf("年份是%d，月份是%d，日期是%d", year, month, day);
 return 0;
}

void date(long input, int* year, int* month, int* day)
{
 *year = (int)(input/ 10000);
 *month = (int)((input - *year * 10000) / 100);
 *day = (int)(input - *year * 10000 - *month * 100);
}
```

* 7.3.7

```c
#include <stdio.h>
#include <math.h>
int main()
{
 float norms(float);
 float pcdif(float, float);
 void showit(float, float);
 void getDate(int*, int*, float*, float*);
 int years, months;
 float height, normht;
 float age, perdif;

 /*这是输入部分*/
 getDate(&years, &months, &height, &age);
 /*这是计算部分*/
 normht = norms(age);
 perdif = pcdif(height, normht);

 /*这是显示部分*/
 showit(normht, perdif);

 return 0;
}

/*下面是norms()的桩函数*/
float norms(float age)
{
 printf("\nInto norms()");
 printf("    age=%f\n", age);
 return (52.5);
}

/*下面是pcdif()函数的桩函数*/
float pcdif(float actual, float normal)
{
 printf("\nInto pcdif()\n");
 printf("    actual=%f   normal=%f\n", actual, normal);
 return(2.5);
}

/*下面是showit()函数的桩函数*/
void showit(float normht, float perdif)
{
 printf("Into showit()\n");
 printf("    normht=%f    perdif=%f\n", normht, perdif);
}
/*下面是getDate()函数*/
void getDate(int* y, int* m, float* height, float* age)
{
 printf("\nHow old (in years) is this child ?\n");
 scanf("%d", y);
 printf("\nHow many months since the child's birthday ?\n");
 scanf("%d", m);
 *age = *y + *m / 12.0;
 printf("Enter the child's height (in inches):");
 scanf("%f", height);
}
```

## 作业9

### 课本10.3

* 10.3.1

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 int ch;
 long int offset, last;
 FILE* inFile;

 outFile = fopen("test.txt", "r");
 if (inFile == NULL)
 {
  printf("\nFailed to open the test.dat file.\n");
  exit(1);
 }
 fseek(inFile, 0L, SEEK_END);
 last = ftell(inFile);
 for (offset = last;offset >= 0;offset--)
 {
  fseek(inFile, offset, SEEK_SET);

  ch = getc(inFile);
  switch (ch)
  {
  case '\n':printf("LF: ");
   break;
  case EOF:printf("EOF:");
   break;
  default:printf("%c:", ch);
   break;
  }
 }
 fclose(inFile);

 return 0;
}
```

* 10.3.2

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 long b;
 FILE* openFile;
 puts("请输入偏移量（相较于末位置）：");
 scanf("%d", &b);
 outFile = fopen("test.txt", "r");
 
 if (abs(fseek(openFile, b, SEEK_END)))
//接收fseek的返回值并进行判断，因为0时是正确执行，所以写在了else里
 {
  puts("Error!");
 }
 else
 {
  puts("That's right!");
 }
 fclose(openFile);
 exit(0);

 return 0;
}
```

### 课本10.4

* 10.4.1

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 char file[51];
 int fcheck(char[]);

 puts("请输入你想要查找的文件名：");
 gets(file);
 printf("返回值为%d", fcheck(file));
 
 return 0;
}

int fcheck(char name[])
{
 FILE* findFile;
 findFile = fopen(,name, "r");
 if (findFile == NULL)
 {
  return 0;
 }
 else
 {
  return 1;
 }
}
```

### 课本11.1

* 11.1.1.a

```c
#include <stdio.h>

int main()
{
 char* ch;
 char samtest[] = "This is a sample";
 for (int i = 0;samtest[i] != 0;i++)
 {
  ch = samtest;
  printf("%c\n", *(ch + i));
 }
 return 0;
}
```

* 11.1.1.b

```c
#include <stdio.h>

int main()
{
 char* ch;
 char samtest[] = "This is a sample";
 for (int i = 10;samtest[i] != 0;i++)
 {
  ch = samtest;
  printf("%c\n", *(ch + i));
 }
 return 0;
}
```

### 课本11.2

* 11.2..2.a

```c
#include <stdio.h>

int main()
{
 int i;
 float* dispPt;
 float rates[] = { 6.25,6.50,6.8,7.2,7.35,7.5,7.65,7.8,9.2,9.4,9.6,9.8,9.0 };
 for (i = 0,dispPt = rates;i < (sizeof(rates) / 4);i++)
 {
  printf("%-5.2f", *dispPt++);
 }
 return 0;
}
```

* 11.2.2.b

```c
#include <stdio.h>

int main()
{
 int i=0;
 float rates[] = { 6.25,6.50,6.8,7.2,7.35,7.5,7.65,7.8,9.2,9.4,9.6,9.8,9.0 };
 float* dispPt = rates;
 while(i < (sizeof(rates) / 4))
    {
  printf("%-5.2f", *dispPt++);
  i++;
 }
 return 0;
}
```

### 课本11.3

* 11.3.2.(1)

```c
#include <stdio.h>

void* findKey(char* select)
{
 printf("%s\n", select);
 return NULL;
}

int main()
{
 char keys[256]="This is a key.";
 printf("%p",findKey(keys));//为了显示出来返回值
 return 0;
}
```

* 11.3.2.(2)

```c
#include <stdio.h>

void* findKey(char select[256])
{
 printf("%s\n", select);
 return NULL;
}

int main()
{
 char keys[256]="This is a key.";
 printf("%p",findKey(keys));//为了显示出来返回值
 return 0;
}
```

* 11.3.2.(3)

```c
#include <stdio.h>

int* findKey(char select[256])
{
 printf("%s\n", select);
 return NULL;
}

int main()
{
 char keys[256]="This is a key.";
 printf("%p",findKey(keys));//为了显示出来返回值
 return 0;
}
```

### 课本11.4

* 11.4.5

```c
#include <stdio.h>
#include <string.h>

int main()
{
 void remove(char message[], char);
 char message[] = "This is a sample";
 remove(message, 'a');
 puts(message);
 return 0;
}

void remove(char message[], char element)
{
 int i = 0, j = 0;
 while (i++ < strlen(message))
 {
  if (element == message[i]);
  else
  {
   message[j++] = message[i];
  }
 }
 message[j] = '\0';
}
```

## 作业10

### 自己编写一个strlen函数，用以计算一个字符串的长度

```c
#include <stdio.h>
void main()
{
 int strlen(char[]);
 char str[50];
 printf("请输入字符串：");
 gets_s(str);
 strlen(str);
 printf("该字符串的长度为%d", strlen(str));
}

int strlen(char string[])
{
 int i = 0;
 while (string[++i] != '\0')
 {
 }
 return i;
}
```

### 课本9.1

* 9.1.2

```c
#include <stdio.h>
#include <string.h>

int main()
{
 void vowels(char[]);
 char a[60];
 gets(a);
 vowels(a);
}

void vowels(char strng[])
{
 int i = 0, a[5] = { 0 };
 char c;
 while ((c = strng[i++] )!= '\0')
 {
  switch (c)
  {
  case 'a':
   a[0]++;
   break;
  case 'e':
   a[1]++;
   break;
  case 'i':
   a[2]++;
   break;
  case 'o':
   a[3]++;
   break;
  case 'u':
   a[4]++;
   break;
  }
 }
 printf("a:%d\te:%d\ti:%d\to:%d\tu:%d\t", a[0], a[1], a[2], a[3], a[4]);
}
```

* 9.1.7

```c
#include <stdio.h>
#include <string.h>

void main()
{
 void delChar(char[], int, int);
 char input[50];
 int length, start;
 printf("请输入原字符串:");
 gets(input);

 printf("请输入被删除字符串的起始位置：");
 scanf("%d",&start);
 
 printf("请输入被删除的字符串长度:");
 scanf("%d", &length);
 
 delChar(input, length, start);
}

void delChar(char base[], int length, int start)
/*题干意思即是说从第start个数开始（含start），将之后的length个数忽略，之后的再接上*/
/*这里直接用i表示output的下标，进行一整个流程的顺序循环*/
{
 int i = 0;
 char output[50];
 while (i<strlen(base)-length)//贯穿整个循环的标准就是i小于base-length的长度
 {
  if (i < start - 1)
  {
   output[i] = base[i];
   i++;
  }
  else if (i >= start - 1)
  {
   output[i] = base[i + length];
   i++;
  }
 }
 output[i] = '\0';
 puts(output);
}
```

* 9.1.8

```c
#include <stdio.h>
#include <string.h>
void main()
{
 void addChar(char[], char[], int);
 char input[50],newstr[50];
 int start;
 printf("请输入原字符串:");
 gets(input);

 printf("请输入插入字符串：");
 gets(newstr);
 
 printf("请输入插入字符串的起始位置:");
 scanf("%d", &start);
 
 addChar(input, newstr, start);
}
void addChar(char base[], char newstr[], int start)
/*题干意思即是说将新字符串在原字符串的第start处开始，后面的接上*/
/*这里仍然用i表示output的下标，进行一整个流程的顺序循环，*/
{
 int i = 0, j = 0;
 char output[50];
 while (i<=strlen(base)+strlen(newstr))//贯穿整个循环的标准就是i小于base+strlen(newstr)的长度
 {
  if (i < start - 1)
  {
   output[i] = base[i];
   i++;
  }
  else if (i >= start - 1 && i < start + strlen(newstr) - 1)
  {
   output[i] = newstr[j];
   i++;
   j++;
  }
  else
  {
   output[i] = base[i - strlen(newstr) ];
   i++;
  }
 }
 output[i] = '\0';
 puts(output);
}
```

### 编写一个函数，统计并输出输入的字符串中：各个数字的个数、字母总个数、特殊字符总个数

```c
#include <stdio.h>
#include <string.h>
void main()
{
 void charnum(char[]);
 char test[100];
 printf("请输入想要进行统计的字符串：\n");
 gets(test);
 charnum(test);
}

void charnum(char test[])
{
 int i, a[12] = { 0 };
//约定a[0]-a[9]分别表示0-9的个数，a[10]表示字母个数、a[11]表示特殊符号的个数
 for (i = 0;i < strlen(test);i++)
 {
  if (test[i] > 47 && test[i] <= 57)//数字
  {
   switch (test[i])//数字细分
   {
   case '0':
    a[0]++;
    break;
   case '1':
    a[1]++;
    break;
   case '2':
    a[2]++;
    break;
   case '3':
    a[3]++;
    break;
   case '4':
    a[4]++;
    break;
   case '5':
    a[0]++;
    break;
   case '6':
    a[6]++;
    break;
   case '7':
    a[7]++;
    break;
   case '8':
    a[8]++;
    break;
   case '9':
    a[9]++;
    break;
   }
  }
  else if (test[i] > 64 && test[i] <= 90 || test[i] > 96 && test[i] <= 122)//字母
   a[10]++;
  else//特殊符号（含空格）
   a[11]++;
 }
 printf("字母：%d\n特殊符号：%d\n",a[10],a[11]);
 printf("0~9的个数分别为：\n");
 for (i = 0;i < 10;i++)
 {
  printf("%d：%d\n", i, a[i]);
 }
}
```

### 课本10.2

* 10.2.8

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 FILE* outFile;
 char No1[6] = "QA310";
 char No2[6] = "CM145";
 char No3[6] = "MS514";
 char No4[6] = "EN212";
 char* PartNumber[4] = { No1,No2,No3,No4 };
 int InitialAmount[4] = { 95,320,34,163 };
 int QuantitySold[4] = { 47,162,20,150 };
 int MinimumAmount[4] = { 50,200,25,160 };
 int i;
 outFile = fopen("file.txt", "w+");
 fprintf(outFile,"%-15s%-15s%-15s%-15s\n","PartNumber","InitialAmount","QuantitySold","MinimumAmount");
 for (i = 0;i < 4;i++)
 {
  fprintf(outFile, "%-15s%-15d%-15d%-15d\n", PartNumber[i], InitialAmount[i], QuantitySold[i], MinimumAmount[i]);
 }
 fclose(outFile);
 exit(0);
 return(0);
}
```

* 10.2.10.a

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 FILE* outFile;
 int i = 0, j = 0;
 int a[18] = { 5,96,87,78,93,21,4,92,82,85,87,6,72,69,85,75,81,73 };
 outFile = fopen("file.txt", "w+");
 for (i = 0;i < 18;i++)
 {
  fprintf(outFile, "%d  ", a[i]);
 }
 fclose(outFile);
 exit(0);
 return(0);
}
```

* 10.2.10.b

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 FILE* outFile;
 int i = 0, j = 0, k;
 double sum = 0;
 int a[19] = { 5,96,87,78,93,21,4,92,82,85,87,6,72,69,85,75,81,73,0};
 outFile = fopen("file.txt", "w+");
 while (a[i] != EOF && i < 18)
 {
  k = i;
  j = j + a[i] + 1;//j用于记录这一行的下标到何时停止
  while (i < j)
  {
   fprintf(outFile, "%d  ", a[i]);
   i++;
   sum += a[i];
  }
  fprintf(outFile, "平均值为%lf", (sum - a[i])/(j-k-1));
  fprintf(outFile, "\n");
  sum = 0;
 }
 fclose(outFile);
 exit(0);
 return(0);
}
```

### 课本10.3

* 10.3.1

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 int ch;
 long int offset, last;
 FILE* inFile;

 outFile = fopen("test.txt", "r");
 if (inFile == NULL)
 {
  printf("\nFailed to open the test.dat file.\n");
  exit(1);
 }
 fseek(inFile, 0L, SEEK_END);
 last = ftell(inFile);
 for (offset = last;offset >= 0;offset--)
 {
  fseek(inFile, offset, SEEK_SET);

  ch = getc(inFile);
  switch (ch)
  {
  case '\n':printf("LF: ");
   break;
  case EOF:printf("EOF:");
   break;
  default:printf("%c:", ch);
   break;
  }
 }
 fclose(inFile);

 return 0;
}
```

* 10.3.2

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 long b;
 FILE* openFile;
 puts("请输入偏移量（相较于末位置）：");
 scanf("%d", &b);
 outFile = fopen("test.txt", "r");
 
 if (abs(fseek(openFile, b, SEEK_END)))
//接收fseek的返回值并进行判断，因为0时是正确执行，所以写在了else里
 {
  puts("Error!");
 }
 else
 {
  puts("That's right!");
 }
 fclose(openFile);
 exit(0);

 return 0;
}
```

### 课本10.4

* 10.4.1

```c
#include <stdio.h>
#include <stdlib.h>

int main()
{
 char file[51];
 int fcheck(char[]);

 puts("请输入你想要查找的文件名：");
 gets(file);
 printf("返回值为%d", fcheck(file));
 
 return 0;
}

int fcheck(char name[])
{
 FILE* findFile;
 findFile = fopen(,name, "r");
 if (findFile == NULL)
 {
  return 0;
 }
 else
 {
  return 1;
 }
}
```

## 作业11

### 1

```c
#include <stdio.h>

int main()
{
 int i,m,n;//i为行号、m为每行的*的个数、n为每行第一个*前所需的空格数
 for (i = 1;i <= 11;i++)
 {
  for (n = 10;n >= i;n--)
  {
   printf(" ");
  }
  for (m = 1;m <= 2 * i - 1;m++)
  {
   printf("*");
  }
  if (i < 11)
  {
   printf("\n");
  }
  else
  {
  }
 }
 return 0;
}
```

### 2

```c
#include <stdio.h>

int main()
{
 int x, y;//x代表第一个乘数，y代表第二个乘数，同时也是行号
 for (y = 1;y <= 9;y++)
 {
  for (x = 1;x <= y;x++)
  {
   printf("%d*%d=%-2d",x,y,x*y);
   printf("    ");
  }
  if (y < 9)
  {
   printf("\n");
  }
  else
  {
  }
 }
 return 0;
}
```
