package com.company;

import java.util.Random;

public class Game {
    boolean result;//以此进行判断该次的输入是否符合
    Player player = new Player();
    LevelParam levelParam = new LevelParam();

    //输出字符串
    void printStr() {

        Random random = new Random();
        StringBuffer buffer = new StringBuffer();

        //将一些值获取进来作为局部变量
        int strLength = levelParam.getStrLength(player.levelNo);
        int timeLimit = levelParam.getTimeLimit(player.levelNo);
        int perScore = levelParam.getPerScore(player.levelNo);
        int strTimes = levelParam.getStrTimes(player.levelNo);

        //进行字符替换
        for (int i = 0; i < strLength; i++) {
            int rand = random.nextInt(strLength);
            switch (rand) {
                case 0:
                    buffer.append("<");
                    break;
                case 1:
                    buffer.append(">");
                    break;
                case 2:
                    buffer.append("@");
                    break;
                case 3:
                    buffer.append("#");
                    break;
                case 4:
                    buffer.append("$");
                    break;
                case 5:
                    buffer.append("&");
                    break;
                case 6:
                    buffer.append("*");
                    break;
                case 7:
                    buffer.append("π");
            }
        }
        System.out.println(buffer);

        result = player.play(buffer.toString(), timeLimit, perScore, strTimes);//获取本局结果
    }

    void printResult() {
        int timeLimit = levelParam.getTimeLimit(player.levelNo);//获取时限
        if (result) {//判定赢了
            System.out.println("输入正确，您的积分" + player.curScore + "，" + "您的级别" + player.levelNo + "，" + "已用时间" + player.getElapsedTime() + "秒");
        } else if ((player.getCurrentTime().getTime() - player.getStartTime().getTime()) / 1000 > (long) timeLimit) {//判定没赢，是时间超了
            System.out.println("你输入太慢了，已经超时，退出！");
            System.out.println("您的积分" + player.curScore + "，" + "您的级别" + player.levelNo);
            System.exit(1);
        } else {//再else，就是输入错误了
            System.out.println("输入错误，退出！");
            System.out.println("您的积分" + player.curScore + "，" + "您的级别" + player.levelNo);
            System.exit(1);
        }
        if (player.levelNo > levelParam.getMaxLevel()) {//已经大于最高等级了
            System.out.println("您已完成挑战，您的积分" + player.curScore + "，" + "您的级别" + (player.levelNo - 1));
            System.exit(0);
        }
    }
}
