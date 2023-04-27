package com.company;

import java.util.Date;
import java.util.Scanner;

public class Player {
    int levelNo = 1;//玩家当前级别
    int curScore = 0;//玩家当前级别积分
    Date startTime = new Date();//当前级别开始时间，而且通过这种方法的确获取到了真实的启动时间
    Date currentTime;
    long elapsedTime = 0;//当前级别已用时间
    long tempElapsedTime = 0;//用于暂存elapsedTime
    int strTime = 0;//记录本等级的输出次数
    Scanner UserInput = new Scanner(System.in);

    boolean play(String buffer, int timeLimit, int perScore, int strTimes) {//获取一次所需的数据，并且判断本次输入是否正确
        //获取用户输入，返回是否输入正确
        String strInput = UserInput.next();//接收用户输入
        currentTime = new Date();//获取当前时间
        if (strInput.equals(buffer) && (currentTime.getTime() - startTime.getTime()) / 1000 < (long) timeLimit) {//输入正确且时间在范围内

            curScore += perScore;//加分
            elapsedTime += (currentTime.getTime() - startTime.getTime()) / 1000;//当前时间进行累加
            strTime++;//记录输入次数加1

            if (strTime >= strTimes) {//本等级的输入次数够了

                levelNo++;//升级
                startTime = currentTime;//重新匹配等级的开始时间
                tempElapsedTime = elapsedTime;//记录一下现在的已用时间，因为之后elapsedTime会清零，影响对结果的输出
                elapsedTime = 0;//当前持续时间清零
                strTime = 0;//当前输入次数清零
            }

            if (levelNo > 6) {
                System.out.println("您已完成挑战，您的积分" + curScore + "，" + "您的级别" + (levelNo - 1));
                System.exit(0);
            }
            return true;
        } else {//不然就错了
            return false;
        }
    }

    Date getStartTime() {
        return startTime;
    }

    Date getCurrentTime() {
        return currentTime;
    }

    long getElapsedTime() {//获取实际的使用时间
        if (elapsedTime == 0)
            return tempElapsedTime;
        else
            return elapsedTime;

    }
}
