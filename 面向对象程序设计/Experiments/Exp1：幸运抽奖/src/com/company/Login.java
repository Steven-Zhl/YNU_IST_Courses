package com.company;

import java.util.Scanner;

public class Login extends Member{
    void login(){
        String account,password;
        while(true){
            Scanner input=new Scanner(System.in);
            System.out.println("请输入账号：");
            account=input.nextLine();
            System.out.println("请输入密码：");
            password=input.nextLine();
            if(account.equals(accountStorage)&&password.equals(passwordStorage)){

            }
        }
    }
}
