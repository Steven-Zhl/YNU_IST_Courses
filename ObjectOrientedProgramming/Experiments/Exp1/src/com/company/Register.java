package com.company;

import java.util.Scanner;

public class Register extends Member{
    String next;
    void register() {
        while (true) {
            System.out.println("请输入个人注册信息：");
            System.out.print("用户名：");
            Scanner aNewMember = new Scanner(System.in);
            accountStorage = aNewMember.nextLine();
            System.out.print("密码：");
            passwordStorage = aNewMember.nextLine();
            state = true;
            System.out.println("\n注册成功，请记好您的会员卡号");

            System.out.println("继续吗？（y/n）");
            Scanner inputChoice2 = new Scanner(System.in);
            next = inputChoice2.nextLine();
            if (next.equals("y")) {
                break;
            } else if (next.equals("n")) {
                System.out.println("系统退出，谢谢使用");
                System.exit(0);
            } else {
                System.out.println("您的输入有误！");
            }
        }
    }
}
