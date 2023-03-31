
#include <stdlib.h>
#include <string.h>
#include "stm32f10x.h" //包含stm32库系统头文件
#include "servor.h"	   //包含GPIO库头文件
#include "usart.h"	   //包含串口通信设置头文件
#include "delay.h"	   //包含系统定时器库头文件
#include "timer.h"	   //包含定时器设置头文件
#include "PS2.h"
#include "key.h"
#include "led.h"
#include "beep.h"
#include "common.h"
#include "adc.h"
#include "motor.h"
#include "control_app.h"
#include "oled.h"
#include "show.h"
#include "encoder.h"
#include "math.h"
int Motor_A, Motor_B, Target_A = 50, Target_B = 50; //电机舵机控制相关
int Voltage_Temp, Voltage_Count, Voltage_All, sum;
int Voltage; //电池电压采样相关的变量
u32 value;
u32 key, key_bak;
extern u32 a; // a用来计数，配合系统滴答定时器可检测代码运行时间
extern uint8 flag_RecFul;
int Encoder_Left, Encoder_Right; //左右编码器的脉冲计数
int Encoder_A_EXTI;
uint16 CPWM[MOTOR_NUM] = {1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500};
char redata[500] = {0}; // 定义接收数据变量数组
uint16 adc_value = 0;
unsigned char flag_scan_ps2 = 0;
u8 LX_AD = 0;
u8 LY_AD = 0;
u8 RX_AD = 0;
u8 RY_AD = 0;
int Motor_Pwm = 6900;
u8 ps2_mode = 0;
char menu = 0;
int i = 0; // sin move count
u8 delay_50, delay_flag;
void scan_ps2(void);
void Check_Power(void);
void ps2_handle(void);
void Check_Battery(void);
/**********************************************************************************/
/*****************************主函数***********************************************/
int main(void)
{
	SysTick_Init();		  //系统滴答定时器初始化
	Servor_GPIO_Config(); // GPIO初始化
	Uart_Init(2);
	Uart_Init(3);
	Timer_Init(); //定时器初始化
	Timer_ON();	  //开启定时器
	LED_Init();
	// KEY_Init();
	Beep_Init();
	Uart_Init(1);
	PS2_Init();
	OLED_Init(); //=====OLED初始化
	Encoder_Init_TIM3();
	Encoder_Init_TIM_Exit0();
	Encoder_Init_TIM_Exit1();
	Adc_Init();
	USART_Config(USART1, 115200);
	USART_Config(USART2, 115200);
	USART_Config(USART3, 115200);
	Motor_Gpio_init();
	PWM2_Init(7199, 0); // 初始化电机工作频率 72/(5+1)  12KHZ
	Led_Test();
	Beep_Test();

	while (1)
	{
		Check_Battery(); //=====读取电池电压
		scan_ps2();
		oled_show(); //===显示屏打开
		delay_flag = 1;
		delay_50 = 0;
		while (delay_flag)
			; //通过定时中断实现的50ms精准延时
	}
}

void Check_Battery(void)
{
	Voltage_Temp = Get_battery_volt(); //=====读取电池电压
	Voltage_Count++;				   //=====平均值计数器
	Voltage_All += Voltage_Temp;	   //=====多次采样累积
	if (Voltage_Count == 10)
		Voltage = Voltage_All / 10, Voltage_All = 0, Voltage_Count = 0; //=====求平均值
}

/******  重点！！！
一次处理后的摇杆值
		LX_AD 0-255 左摇杆x轴
		LY_AD 0-255 左摇杆y轴
		RX_AD 0-255 右摇杆x轴
		RY_AD 0-255 右摇杆y轴
转弯函数
	CPWM[1]=1500;正中央（数值范围500-2500）
前进函数
		Set_Pwm_Motor1(0);最大值限制为7000
		Set_Pwm_Motor2(0);
******/

void scan_ps2(void)
{
	if (flag_scan_ps2) //
	{
		flag_scan_ps2 = 0;
		key = PS2_DataKey();
		// Gain LX_AD,RY_AD and so on
		LX_AD = PS2_AnologData(PSS_LX);
		RY_AD = PS2_AnologData(PSS_RY);
		// UART_Put_Inf("LY_AD:",LY_AD);
		ps2_mode = PS2_RedLight();

		if (ps2_mode == 0)
		{
			//注意一定要处理先获得DEAL_RY_AD、DEAL_RX_AD的值(两个值目前没有定义)

			Set_Pwm_Motor1((RY_AD - 255 / 2) * 25);
			Set_Pwm_Motor2((RY_AD - 255 / 2) * 25);
			CPWM[1] = LX_AD * 2000 / 255 + 500;

			switch (key) //此为参考，不一定要这样用if等也行
			{
			case PSB_PAD_UP:
				Set_Pwm_Motor1(5000); //电机设置
				Set_Pwm_Motor2(5000);
				break;
			case PSB_PAD_DOWN:
				Set_Pwm_Motor1(-5000); //电机设置
				Set_Pwm_Motor2(-5000);
				break;
			case PSB_PAD_LEFT:
				CPWM[1] = 1000; //左转一个角度
				break;
			case PSB_PAD_RIGHT:
				CPWM[1] = 1500 + LX_AD * 1000 / 255; //右转合适角度(从中间开始)
				break;
			case PSB_TRIANGLE:
				break;
			case PSB_CROSS:
				break;
			case PSB_PINK:
				break;
			case PSB_CIRCLE:
				break;
			case PSB_L1:
				break;
			case PSB_L2:
				break;
			case PSB_R1:
				break;
			case PSB_R2:
				break;
			default:
				break;
			}
			/******
			一次处理后的摇杆值
					LX_AD 0-255 左摇杆x轴
					LY_AD 0-255 左摇杆y轴
					RX_AD 0-255 右摇杆x轴
					RY_AD 0-255 右摇杆y轴
			转弯函数
				CPWM[1]=1500;正中央（数值范围500-2500）
			前进函数
					Set_Pwm_Motor1(0);最大值限制为7000
					Set_Pwm_Motor2(0);
			******/
		}
		else // PS2为其他模式
		{
			switch (key) //此为参考，不一定要这样用if等也行
			{
			case PSB_PAD_UP:
				break;
			case PSB_PAD_DOWN:
				break;
			case PSB_PAD_LEFT:
				break;
			case PSB_PAD_RIGHT:
				break;
			case PSB_TRIANGLE:
				//运动模式=圆周
				Set_Pwm_Motor1(5000); //电机设置
				Set_Pwm_Motor2(5000);
				CPWM[1] = 2300; //左转一个角度
				break;
			case PSB_CROSS:
				//运动模式=静止
				Set_Pwm_Motor1(0); //电机设置
				Set_Pwm_Motor2(0);
				CPWM[1] = 1500; //左转一个角度
				break;
			case PSB_SQUARE:
				break;
			case PSB_CIRCLE:
				//运动模式=随意(自行设定)
				while (1)
				{
					int angle = (int)(1000 * sin(i * 3.14159 / 180)) + 1500; // 计算前轮的转向角度
					CPWM[1] = angle;										 // 将转向角度传入底盘控制函数
					Set_Pwm_Motor1(2500);
					Set_Pwm_Motor2(2500);
					key = PS2_DataKey();
					if (key == PSB_CROSS)
						break;
					// 决定前进还是后退，并控制角度
					Delay_ms(5); // 信号间隔5ms，此时前轮转向周期约为1.8s，后轮转换一次方向约为5s
					i++;
				}
				break;
			case PSB_L1:
				break;
			case PSB_L2:
				break;
			case PSB_R1:
				break;
			case PSB_R2:
				break;
			default:
				break;
			}
		}
	}
}
