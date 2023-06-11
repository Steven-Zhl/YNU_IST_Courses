package com.company;

public class Main {
    public static void main(String[] args) {
        Menu welcome = new Menu();
        welcome.menu();
        if (welcome.choice == 1) {//选择注册
            Register addNewOne = new Register();
            addNewOne.register();
            Login newOne=new Login();
            newOne.login();
        } else if (welcome.choice == 2) {//选择登录
            Login login =new Login();
            login.login();
        } else if (welcome.choice == 3) {//选择抽奖
            LuckDraw luckDraw=new LuckDraw();
            luckDraw.luckDraw();
        }
        welcome.menu();
    }
}