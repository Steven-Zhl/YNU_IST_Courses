package com.company;

import java.util.Scanner;

public class Menu {
    int choice;
    String next;

    void menu() {
        while (true) {
            System.out.println("*****欢迎进入奖客富翁系统*****");
            System.out.println("          1.注册");
            System.out.println("          2.登录");
            System.out.println("          3.抽奖");
            System.out.println("**************************");
            System.out.print("请选择菜单：");
            Scanner inputChoice = new Scanner(System.in);
            choice = inputChoice.nextInt();
            if (choice == 1) {
                System.out.println("[奖客富翁系统 > 注册]");
            } else if (choice == 2) {
                System.out.println("[奖客富翁系统 > 登录]");
            } else if (choice == 3) {
                System.out.println("[奖客富翁系统 > 抽奖]");
            } else {
                System.out.println("您的输入有误！");
            }
            System.out.println("继续吗？（y/n）");
            Scanner inputChoice2=new Scanner(System.in);
            next = inputChoice2.nextLine();
            if (next.equals("y")) {
                break;
            }
            else if (next.equals("n")) {
                System.out.println("系统退出，谢谢使用");
                System.exit(0);
            }
            else{
                System.out.println("您的输入有误！");
            }
        }
    }
}