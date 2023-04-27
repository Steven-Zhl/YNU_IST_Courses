package com.company;

import java.util.Scanner;

public class Game {

    String nextStep;//用于记录每次选择y/n的结果
    String opponentName, userName;//分别暂存双方的名字

    void initial() {
        int characterNumber;//character仅在本方法中存在，用于记录玩家选择的角色代号，因为有可能在之后选择n，所以暂不写入User类

        System.out.println("----------------欢 迎 进 入 游 戏 世 界----------------");
        System.out.println("           ******************");
        System.out.println("           **   猜拳，开始   **");
        System.out.println("           ******************");
        System.out.print("\n");
        System.out.println("出拳规则：1. 剪刀 2. 石头 3.布");
        Scanner input = new Scanner(System.in);//input对象使用两次，分别接收对方的角色和玩家的名字

        System.out.print("请选择对方角色：（1. 刘备 2. 孙权 3. 曹操）：");
        characterNumber = input.nextInt();

        System.out.print("请输入你的姓名：");
        userName = input.next();

        //下面对用户的输入作整理并输出情况
        if (characterNumber == 1) {
            opponentName = "刘备";
            System.out.println(userName + " VS " + opponentName + " 对战");
        } else if (characterNumber == 2) {
            opponentName = "孙权";
            System.out.println(userName + " VS " + opponentName + " 对战");
        } else if (characterNumber == 3) {
            opponentName = "曹操";
            System.out.println(userName + " VS " + opponentName + " 对战");
        }

        //下面让用户选择是否继续
        while (true) {
            System.out.print("要开始吗？（y/n）");
            nextStep = input.next();
            if (nextStep.equals("y")) {
                nextStep = null;
                break;
            } else if (nextStep.equals("n")) {
                System.out.println("那就结束吧！");
                System.exit(0);
            } else {
                System.out.println("您的输入有误,请重试！");
            }
        }
    }

    void startGame() {
        int fistNumber;//记录用户出拳的编号
        int i = 0;//记录比赛场数

        //既然已经确定猜拳了，就将之前用户的输入写入对应对象的成员变量中
        User player = new User();
        player.name = userName;
        Computer opponent = new Computer();
        opponent.name = opponentName;

        Scanner input = new Scanner(System.in);//这个对象用于接收各种输入

        while (true) {
            System.out.print("请出拳：1. 剪刀 2. 石头 3. 布 （输入相应数字）：");
            fistNumber = input.nextInt();//用于接收选择用户出拳的编号

            System.out.println("你出拳：" + player.showFist(fistNumber));
            System.out.println("电脑出拳：" + opponent.showFist());

            //下面是对结果的判断：编号相等即平局，差的绝对值为1谁大谁赢，差的绝对值为2谁小谁赢
            if (opponent.fistNumber == player.fistNumber) {
                System.out.println("结果：和局，真衰！嘿嘿，等着瞧吧！");
            } else if (Math.abs(player.fistNumber - opponent.fistNumber) == 1) {
                if (player.fistNumber > opponent.fistNumber) {
                    System.out.println("恭喜，你赢了！");
                    User.score++;
                } else {
                    System.out.println("^__^你输了，真笨！");
                    Computer.score++;
                }
            } else {
                if (player.fistNumber < opponent.fistNumber) {
                    System.out.println("恭喜，你赢了！");
                    User.score++;
                } else {
                    System.out.println("^__^你输了，真笨！");
                    Computer.score++;
                }
            }

            System.out.println("是否开始下一轮（y/n）");
            nextStep = input.next();
            if (nextStep.equals("y")) {
                nextStep = null;
                i++;//记录比赛场次
            } else if (nextStep.equals("n")) {
                break;
            } else {
                System.out.println("您的输入有误,请重试！");
            }
        }

        System.out.println(player.name + " VS " + opponent.name);
        System.out.println("\n对战次数：" + ++i);
        if (User.score == Computer.score) {
            System.out.println("结果：打成平手，下次再和你一分高下！");
        } else if (User.score > Computer.score) {
            System.out.println("你赢了，好强啊！");
        } else {
            System.out.println("结果：呵呵，笨笨，继续加油啊");
        }
    }
}