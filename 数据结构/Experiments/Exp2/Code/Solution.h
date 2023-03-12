#ifndef __SOLUTION_H__
#define __SOLUTION_H__
typedef struct student_message
{
	char *ID;			 //学号
	double chineseScore; //语文
	double mathScore;	 //数学
	double englishScore; //英语
	double totalScore;	 //总分
	double aveScore = 0; //加权平均分
	//计算加权平均分
	void calcAveScore()
	{
		aveScore = chineseScore * 0.3 + mathScore * 0.5 + englishScore * 0.2;
	}
	//计算总分
	void calcTotalScore()
	{
		totalScore = chineseScore + mathScore + englishScore;
	}
	void printStuMes()
	{
		printf("  学号：%s\n", ID);
		printf("  语文成绩：%5.2lf\n", chineseScore);
		printf("  数学成绩：%5.2lf\n", mathScore);
		printf("  英语成绩：%5.2lf\n", englishScore);
		printf("  总成绩：%5.2lf\n", totalScore);
		printf("  加权平均分：%5.2lf\n", aveScore);
	}
} student;

int question4()
{
	int power_num; //阶数
	double x, result = 0, *para;
	double power(double x, int power); //函数头声明
	printf("请输入多项式的次数：");
	scanf("%d", &power_num);
	para = (double *)malloc((power_num + 1) * sizeof(double));
	for (int i = 0; i < power_num + 1; i++)
	{
		printf("请输入%d次项的系数，如无则填0：", i);
		scanf("%lf", &para[i]);
	}
	printf("请输入未知量的赋值:");
	scanf("%lf", &x);
	for (int i = 0; i < power_num + 1; i++)
	{
		result += para[i] * power(x, i);
	}
	printf("%lf", result);
}

double power(double x, int pow_num)
{
	if (pow_num == 0)
		return 1;
	else
		return x * power(x, pow_num - 1);
}
#endif