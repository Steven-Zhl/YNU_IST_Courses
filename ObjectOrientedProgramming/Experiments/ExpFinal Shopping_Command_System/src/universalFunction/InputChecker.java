package pers.Steven.shoppingManagementSystem.universalFunction;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class InputChecker {
    Scanner input = new Scanner(System.in);

    //检测选择是否符合范围以及是否符合要求（出现0表示错误，范围为1~totalSwitch）
    public int checkSwitchRange(int totalSwitch) {
        int choice;
        if (input.hasNextInt()) {
            choice = input.nextInt();
        } else {
            System.out.println("您的输入有误，请重试");
            return 0;
        }

        if (choice <= totalSwitch && choice > 0) {
            return choice;
        } else {
            System.out.println("您的输入有误，请重试");
            return 0;
        }
    }

    //在重要操作时进行二次警告（出现错误之后取消操作）
    public boolean alertAndConfirm() {
        int choice;
        System.out.println("您是否确定该操作？");
        System.out.println("1. 确定   2. 取消");
        //需要测试
        if (input.hasNextInt()) {
            choice = input.nextInt();
            if (choice == 1)
                return true;
            else if (choice == 2)
                return false;
            else {
                System.out.println("您的输入有误，操作已取消");
                return false;
            }
        } else {
            System.out.println("您的输入有误，操作已取消");
            return false;// 相当于取消该操作
        }
    }

    //检查字符串是否可用作密码
    public boolean checkPasswordLegality(String inputPassword) {//长度大于8，必须是大小写字母、数字和标点符号的组合。
        boolean lengthLimit;
        boolean kindsLimit;

        int[] everyKindsNum = new int[4];//四个值分别对应大写、小写、数字、符号的个数
        //判断长度是否可行
        lengthLimit = inputPassword.length() > 8;

        for (int i = 0; i < inputPassword.length(); i++) {
            char temp = inputPassword.charAt(i);
            if (Character.isUpperCase(temp)) {
                everyKindsNum[0]++;
            } else if (Character.isLowerCase(temp)) {
                everyKindsNum[1]++;
            } else if (Character.isDigit(temp)) {
                everyKindsNum[2]++;
            } else {
                everyKindsNum[3]++;
            }
        }
        kindsLimit = everyKindsNum[0] * everyKindsNum[1] * everyKindsNum[2] * everyKindsNum[3] != 0;
        return lengthLimit && kindsLimit;
    }

    //检测字符串是否可用作账号
    public boolean checkAccountLegality(String inputAccount, File UserAccountsFilePath) {//账号不重、长度大于等于5
        FileReader accountFile;//创建一个读取文件的指针
        BufferedReader readAccount;//读取指针的文件流的对象
        String thisLineMessage;//获取每一行

        try {
            accountFile = new FileReader(UserAccountsFilePath);
            readAccount = new BufferedReader(accountFile);
            thisLineMessage = readAccount.readLine();
            while (thisLineMessage != null) {
                String thisAccount = thisLineMessage.split("~")[0];
                if (inputAccount.equals(thisAccount)) {//如果与某个账号重复了，则直接判定不能作为账号，返回false
                    return false;
                } else {
                    thisLineMessage = readAccount.readLine();
                }
            }
            accountFile.close();
            accountFile.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        //在第一个比较结束后进行判定长度，若符合大于5则已经符合所有要求，返回true
        return inputAccount.length() >= 5;
    }

    //检查字符串是否可以作为邮箱地址
    public boolean checkMailLegality(String inputMail) {
        if (inputMail == null)
            return false;
        String rule = "[\\w!#$%&'*+/=?^_`{|}~-]+(?:\\.[\\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\\w](?:[\\w-]*[\\w])?\\.)+[\\w](?:[\\w-]*[\\w])?";
        Pattern pattern;
        Matcher matcher;
        pattern = Pattern.compile(rule);
        matcher = pattern.matcher(inputMail);
        return matcher.matches();
    }

    //检查字符串是否可以作为手机号
    public boolean checkTelephoneLegality(String inputTelephone) {
        if (inputTelephone.length() != 11) {
            return false;
        }
        if (inputTelephone.charAt(0) != '1') {
            return false;
        }
        for (int i = 0; i < inputTelephone.length(); i++) {
            if (!Character.isDigit(inputTelephone.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    //获取输入的字符串内容，主要作用是防止输入有误
    public String getInputString() {
        String inputContents;
        if (input.hasNext()) {
            inputContents = input.next();
        } else {
            System.out.println("您的输入有误，请重试！");
            return null;
        }
        return inputContents;
    }
}
