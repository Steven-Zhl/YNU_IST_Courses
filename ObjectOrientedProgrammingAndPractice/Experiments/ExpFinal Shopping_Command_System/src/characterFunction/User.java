package pers.Steven.shoppingManagementSystem.characterFunction;

import pers.Steven.shoppingManagementSystem.universalFunction.InputChecker;
import pers.Steven.shoppingManagementSystem.universalFunction.Item;
import com.sun.mail.util.MailSSLSocketFactory;

import java.io.*;
import java.security.GeneralSecurityException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import javax.mail.*;
import javax.mail.internet.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.Properties;

public class User extends Person {
    private int level;//账户等级
    private Date registerTime;//注册日期
    private float totalCost;//总消费
    private String telephone;//手机号
    private String mail;//邮箱
    boolean registerState = false;//注册状态
    private ArrayList<Item> curt = new ArrayList<>();
    private ArrayList<String> shoppingHistory = new ArrayList<>();//购物历史不会改动，故设为String类型即可
    InputChecker inputChecker = new InputChecker();

    //构造方法
    public User(String account, String password) {
        this.account = account;
        this.password = password;
    }

    //构造方法
    public User(String choice) {
        switch (choice) {
            case "登录" -> {
                //循环5次的操作
                for (int i = 0; i < 5; i++) {
                    loginState = login();
                    if (getLoginState()) {
                        break;
                    } else {
                        System.out.println("输入错误，您还有" + (4 - i) + "次机会");
                    }
                }

                if (getLoginState()) {
                    //以下待测试
                    initializeUserMessage();//初始化用户账户数据，写完了
                    initializeShoppingHistory();//初始化购物历史，写完了
                    initializeShopping();//初始化商城数据，写完了
                    initializeCurtData();// 初始化购物车
                } else {
                    System.out.println("您已连续输入错误5次，该账户已锁定");
                }
            }
            case "注册" -> register();
            case "找回密码" -> {
                try {
                    findPassword();
                } catch (IOException | MessagingException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    //注册
    private void register() {
        boolean accountLegal, passwordLegal;//判断设定的账号密码是否合法
        String inputAccount, inputPassword;

        //获取输入信息
        System.out.print("请输入您的账号：");
        inputAccount = inputChecker.getInputString();
        System.out.println("您输入的账号为：" + inputAccount);
        System.out.print("请输入您的密码:");
        inputPassword = inputChecker.getInputString();
        System.out.println("您输入的密码为：" + inputPassword);

        //在开始注册流程之前进行二次确认
        boolean confirmSituation = inputChecker.alertAndConfirm();
        if (!confirmSituation) {//输入不合法或取消注册则直接返回
            System.out.println("您已取消注册，即将返回上级菜单");
            return;
        }

        //检测输入的账号密码是否合法以及对不合法的给出提示
        accountLegal = inputChecker.checkAccountLegality(inputAccount, USER_ACCOUNT_LIST_FILE);//检查账号是否合法
        passwordLegal = inputChecker.checkPasswordLegality(inputPassword);//检查密码是否合法

        if (!accountLegal && !passwordLegal) {
            System.out.println("您的账号和密码设置均不合法，请检查以下可能的问题后重试：");
            System.out.println("账号：不与已存在账号重复，且长度不少于5个字符");
            System.out.println("密码：长度大于8个字符，且必须包含大小写字母、数字和标点符号");
            return;
        } else if (!accountLegal && passwordLegal) {
            System.out.println("您的账号设置不合法，请检查以下可能的问题后重试：");
            System.out.println("账号：不与已存在账号重复，且长度不少于5个字符");
            return;
        } else if (accountLegal && !passwordLegal) {
            System.out.println("您的密码设置不合法，请检查以下可能的问题后重试：");
            System.out.println("密码：长度大于8个字符，且必须包含大小写字母、数字和标点符号");
            return;
        }

        //审核通过，初始化个人信息
        Date now = new Date();
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String registerTime = dateFormat.format(now);
        String telephone, mail;
        File accountFile = getPersonalAccountMessageFile(inputAccount);
        BufferedWriter writeAccountMessage;

        System.out.print("请输入您的手机号码：");
        telephone = inputChecker.getInputString();
        System.out.print("请输入您的邮箱：");
        mail = inputChecker.getInputString();
        if (!(inputChecker.checkTelephoneLegality(telephone) && inputChecker.checkMailLegality(mail))) {
            System.out.println("您的手机号码或邮箱格式错误，注册未成功");
            return;
        }

        // 初始化个人信息文件
        try {
            accountFile.createNewFile();
            writeAccountMessage = new BufferedWriter(new FileWriter(accountFile));
            writeAccountMessage.write("用户名：" + inputAccount + "\n" + "等级：0\n" + "注册时间：" + registerTime + "\n" + "总消费金额：0\n" + "手机号码：" + telephone + "\n" + "邮箱地址：" + mail + "\n");
            writeAccountMessage.flush();
            writeAccountMessage.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // 创建个人购物车和购物历史文件
        File curtFile = getPersonalAccountCurtFile(inputAccount);
        File historyFile = getPersonalAccountHistoryFile(inputAccount);
        try {
            curtFile.createNewFile();
            historyFile.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }

        //更新账号库的内容（write方法使用append类型，即在文末添加）
        inputPassword = getMD5String(inputPassword);
        FileWriter writer;
        try {
            writer = new FileWriter(USER_ACCOUNT_LIST_FILE, true);
            writer.write(inputAccount + "~" + inputPassword + "\n");
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        registerState = true;
        System.out.println("注册成功，欢迎使用");
    }

    // 初始化：账户基础信息
    public void initializeUserMessage() {//将获取到的字符串进行截取，以取得正确的各项信息
        ArrayList<String> property = getEveryLineMessageFromFile(getPersonalAccountMessageFile());
        setLevel(property.get(1).substring(3));
        setRegisterTime(property.get(2).substring(5));
        setTotalCost(property.get(3).substring(6));
        setTelephone(property.get(4).substring(5));
        setMail(property.get(5).substring(5));
    }

    // 初始化：购物历史记录
    public void initializeShoppingHistory() {
        ArrayList<String> items = getEveryLineMessageFromFile(getPersonalAccountHistoryFile());
        shoppingHistory.addAll(items);
    }

    // 初始化：购物车信息
    public void initializeCurtData() {
        ArrayList<String> items = getEveryLineMessageFromFile(getPersonalAccountCurtFile());
        for (String item : items) {
            curt.add(new Item(item));
        }
    }

    // 功能菜单：显示用户信息
    public void showAllMessage() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        System.out.println("---------用户信息---------");
        System.out.println("\t用户名：" + getAccount());
        System.out.println("\t用户等级：" + (level == 0 ? ("铜牌客户") : (level == 1 ? ("银牌客户") : ("金牌客户"))));
        System.out.println("\t用户注册时间：" + sdf.format(registerTime));
        System.out.println("\t累积消费金额：" + totalCost);
        System.out.println("\t手机号码：" + telephone);
        System.out.println("\t邮箱：" + mail);
        System.out.println("-------------------------\n");
    }

    // 功能菜单：得到格式化的用户个人账户信息
    public String getAccountWriteInString() {
        return "用户名：" + account + "\n" + "等级：" + level + "\n" + "注册时间：" + getRegisterTime() + "\n" + "总消费金额：" + totalCost + "\n" + "手机号码：" + telephone + "\n" + "邮箱地址：" + mail + "\n";
    }

    //找回密码功能
    public void findPassword() throws IOException, MessagingException {
        String account;//用户输入的他自己的账号
        String userMail;//记录用户的收件邮箱
        String sendMail = "1440864175@qq.com";//发件邮箱
        String sendTsetCode;//验证码
        String getTestCode;//接收用户收到的验证码

        //获取到用户邮箱
        System.out.println("请输入您的账号");
        account = inputChecker.getInputString();
        FileReader accountMessageFile = null;// 文件管理器
        BufferedReader readAccountMessageFile = null;
        if (!getPersonalAccountMessageFile(account).exists()) {
            System.err.println("未找到您的信息，找回密码失败，即将返回主菜单");
            return;
        }
        try {
            accountMessageFile = new FileReader(getPersonalAccountMessageFile(account));
            readAccountMessageFile = new BufferedReader(accountMessageFile);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        String thisLine = null;
        for (int i = 0; i <= 5; i++) {
            thisLine = readAccountMessageFile.readLine();
        }
        userMail = thisLine.substring(5);//获取到用户邮箱
        readAccountMessageFile.close();
        accountMessageFile.close();

        //编辑并发送验证码
        Date now = new Date();
        sendTsetCode = String.valueOf(now.getTime()).substring(7, 13);//验证码是long型发送时间的后6位
        System.out.println("正在向你的邮箱中发送验证码，请稍候...");
        //配置发送客户端
        Properties properties = new Properties();
        properties.setProperty("mail.host", "smtp.qq.com");
        properties.setProperty("mail.transport.protocol", "smtp");
        properties.setProperty("mail.smtp.auth", "true");
        MailSSLSocketFactory sf = null;
        try {
            sf = new MailSSLSocketFactory();
        } catch (GeneralSecurityException e) {
            e.printStackTrace();
        }
        sf.setTrustAllHosts(true);
        properties.put("mail.smtp.ssl.enable", "true");
        properties.put("mail.smtp.ssl.socketFactory", sf);
        //创建一个session对象
        Session session = Session.getDefaultInstance(properties, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication("1440864175@qq.com", "qxgnrksubcuehcji");
            }
        });
        //debug完成，已关闭debug模式
        //session.setDebug(true);
        //获取连接对象
        Transport transport = session.getTransport();
        //连接服务器
        transport.connect("smtp.qq.com", "1440864175@qq.com", "qxgnrksubcuehcji");
        //创建邮件对象
        MimeMessage mimeMessage = new MimeMessage(session);
        //邮件发送人
        mimeMessage.setFrom(new InternetAddress(sendMail));
        //邮件接收人
        mimeMessage.setRecipient(Message.RecipientType.TO, new InternetAddress(userMail));
        //邮件标题
        mimeMessage.setSubject("购物系统：您正在通过绑定邮箱找回账号");
        //邮件内容
        mimeMessage.setContent("<h1>你好，购物系统的用户\n</h1>" + "您正在使用找回密码功能，请记住您的验证码：" + sendTsetCode + " ，并尽快根据验证码完成密码重置。\n" + "如果这并非您的请求，请忽略本消息。\n祝您生活愉快。\n" + "\tSteven", "text/html;charset=UTF-8");
        //发送邮件
        transport.sendMessage(mimeMessage, mimeMessage.getAllRecipients());
        transport.close();

        System.out.print("已发送至您的预留邮箱，请输入您收到的验证码：");
        int loopNum = 0;
        for (; loopNum < 5; loopNum++) {
            getTestCode = inputChecker.getInputString();
            if (getTestCode.equals(sendTsetCode)) {
                System.out.print("验证成功，请输入您的新密码：");
                String newPassword = inputChecker.getInputString();
                if (inputChecker.checkPasswordLegality(newPassword)) {
                    // 该密码可行，就修改相关密码
                    changePassword(account, newPassword);
                    return;
                }
            } else {
                System.out.println("您输入的验证码有误，请重试，您还有" + (5 - loopNum) + "次机会");
            }
        }
        //循环超过5次后到这里
        System.out.println("您输入错误次数过多，验证码失效，请稍后再试");
    }

    // 展示所有购物车中的商品
    public int showAllItemInCurt() {
        int num = 0;
        if (curt.size() == 0) {
            System.out.println("购物车中暂无商品");
        } else {
            for (int index = 0; index < curt.size(); index++) {
                System.out.println("商品序号：" + (index + 1));
                curt.get(index).showAllMessageForUser();
                num++;
            }
        }
        return num;
    }

    // 添加商品到购物车
    public void addItemToCurt() {
        int index, itemNum = 0, num;//index为被添加的商品序号
        // 显示所有商城中的商品
        for (int i = 0; i < MallItems.size(); i++) {
            System.out.println("商品序号：" + (i + 1));
            MallItems.get(i).showAllMessageForUser();
            itemNum++;
        }
        // 选择商品
        System.out.print("请选择要添加到购物车的商品序号：");
        index = inputChecker.checkSwitchRange(itemNum);
        if (index == 0) {
            addItemToCurt();
        }
        index--;

        // 选择数量
        System.out.print("请输入添加的数量：");
        num = inputChecker.checkSwitchRange(MallItems.get(index).getNum());
        if (num == 0) return;

        //满足条件后，将物品添加到购物车，并在商店中删去
        if (num <= MallItems.get(index).getNum() && index < MallItems.size()) {
            String addItemName = MallItems.get(index).getName();
            boolean exist = false;
            for (Item item : curt) {//遍历curt，若购物车中存在，直接添加数量即可
                if (item.getName().equals(addItemName)) {
                    item.setNum(item.getNum() + num);
                    exist = true;
                    break;
                }
            }
            if (!exist) {//如果经过遍历仍然确定不存在，那么需要在curt中添加这一商品
                Item item = new Item();
                item.copy(MallItems.get(index));
                item.setNum(num);
                curt.add(item);
            }
            //在商城中减少对应的数量
            MallItems.get(index).setNum(MallItems.get(index).getNum() - num);
            if (MallItems.get(index).getNum() == 0)
                MallItems.remove(index);
            System.out.println("添加成功，即将返回主菜单");
        } else {
            System.out.println("添加数量大于当前剩余数量，添加无效");
            System.out.println("即将返回菜单");
        }
    }

    public void removeItemInCurt() {
        int ID, curtIndex;
        int itemNum = showAllItemInCurt();

        System.out.print("请选择要删除的物品序号：");
        ID = inputChecker.checkSwitchRange(itemNum);
        if (ID == 0) {
            removeItemInCurt();
        }
        curtIndex = ID - 1;

        System.out.println("您即将移除：" + curt.get(curtIndex).getName());
        boolean confirmPosition = inputChecker.alertAndConfirm();
        if (confirmPosition) {
            int mallIndex = searchItemIndexByName(curt.get(curtIndex).getName());
            if (mallIndex != -1) {
                MallItems.get(mallIndex).setNum(MallItems.get(mallIndex).getNum() + curt.get(curtIndex).getNum());
            } else {//如果购物车中不存在该商品，就新建个该商品，把当前item的信息复制过去
                MallItems.add(new Item(curt.get(curtIndex).getWriteInString()));
            }
            curt.remove(curtIndex);
        } else {
            System.out.println("您已取消移除该项目");
        }
    }

    //删减购物车物品数量
    public void decreaseItemNumInCurt() {
        int index, removeNum;
        int itemNum = showAllItemInCurt();
        System.out.print("请选择要修改数量的物品序号:");
        index = inputChecker.checkSwitchRange(itemNum);
        if (index == 0) {
            decreaseItemNumInCurt();
        }
        index--;//得到真正的ID，也就是index
        System.out.println("您要删减的物品为：" + curt.get(index).getName());

        System.out.print("请输入要删减的数量:");
        removeNum = inputChecker.checkSwitchRange(curt.get(index).getNum());
        if (removeNum != 0 && removeNum < curt.get(index).getNum()) {//正常的删减数量
            // 删减掉购物车中对应的物品数量
            curt.get(index).setNum(curt.get(index).getNum() - removeNum);
            //将物品还到商城中
            int mallIndex = searchItemIndexByName(curt.get(index).getName());//搜索到商品在mall中的index
            if (mallIndex != -1) {
                MallItems.get(mallIndex).setNum(MallItems.get(mallIndex).getNum() + removeNum);
            } else {
                MallItems.add(new Item(curt.get(index).getWriteInString()));
            }
            System.out.println("修改完成，现在数量为" + curt.get(index).getNum());
        } else if (removeNum >= curt.get(index).getNum()) {//删减量大于购物车中的数量，即为删除
            System.out.println("你即将删除：" + curt.get(index).getName());
            boolean confirmPosition = inputChecker.alertAndConfirm();
            //从购物车中移除，那么实际删除数量就是购物车中的数量
            if (confirmPosition) {
                int mallIndex = searchItemIndexByName(curt.get(index).getName());//搜索到商品在mall中的index
                if (mallIndex != -1) {//把数量加上
                    MallItems.get(mallIndex).setNum(MallItems.get(mallIndex).getNum() + curt.get(index).getNum());
                } else {//直接创建一份
                    MallItems.add(new Item(curt.get(index).getWriteInString()));
                }
                curt.remove(index);
            } else {
                System.out.println("该操作已取消");
            }
        }
    }

    //结账
    public void payForCurt() {
        long totalCost = 0;
        int choice;
        boolean payPosition = false;
        for (Item value : curt) {
            totalCost += (long) value.getNum() * value.getSellPrice();
        }
        System.out.println("您需要支付的金额为" + totalCost + "，请选择支付方式:");
        System.out.println("\t1. 微信支付   2. 支付宝   3. 取消支付");
        choice = inputChecker.checkSwitchRange(3);
        switch (choice) {
            case 1 -> {
                System.out.println("您已完成支付，支付方式：微信支付");
                payPosition = true;
            }
            case 2 -> {
                System.out.println("您已完成支付，支付方式：支付宝");
                payPosition = true;
            }
            case 3 -> System.out.println("取消支付成功");
            default -> payForCurt();
        }
        if (payPosition) {
            //写入购物记录
            for (Item item : curt)
                shoppingHistory.add(item.getWriteInString());
            curt.clear();

            if (getLevel() == 0) {// 根据消费额修改等级
                if (getTotalCost() + (int) totalCost > 5000 && getTotalCost() + (int) totalCost <= 10000) {
                    setLevel(1);
                    System.out.println("您已成为银牌客户！");
                } else if (getTotalCost() + (int) totalCost > 10000) {
                    setLevel(2);
                    System.out.println("您已成为金牌客户！");
                }
            } else if (getLevel() == 1) {
                if (getTotalCost() + (int) totalCost > 1000) {
                    setLevel(2);
                    System.out.println("您已成为金牌客户！");
                }
            }
            setTotalCost(getTotalCost() + totalCost);
        }
    }

    //查看所有的购物历史
    public void showTheHistoryOfShopping() {
        System.out.println("----------购-物-记-录----------");
        System.out.println("商品名称 生产厂家 生产日期 型号 销售价格 数量");
        for (String originItemData : shoppingHistory) {
            System.out.println(originItemData.replace('~', ' '));
        }
    }

    //将购物车、购物历史、商城数据写入文件
    public void exitMenu() {
        File curtFile = getPersonalAccountCurtFile(), historyFile = getPersonalAccountHistoryFile();
        //写入购物历史文件
        writeInFile(shoppingHistory, historyFile);
        //创建购物车文本数组，并写入
        ArrayList<String> curtTxt = new ArrayList<>();
        for (Item item : curt) {
            curtTxt.add(item.getWriteInString());
        }
        writeInFile(curtTxt, curtFile);
        //创建商品文本数组，并写入
        ArrayList<String> mallTxt = new ArrayList<>();
        for (Item item : MallItems) {
            mallTxt.add(item.getWriteInString());
        }
        writeInFile(mallTxt, SHOPPING_ITEM_LIST_FILE);
    }

    public void setLevel(String level) {
        this.level = Integer.parseInt(level);
    }

    public void setLevel(int level) {
        this.level = level;
    }

    public int getLevel() {
        return level;
    }

    public String getRegisterTime() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return sdf.format(registerTime);
    }

    public void setRegisterTime(String Time) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        try {
            registerTime = sdf.parse(Time);
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

    public void setTotalCost(String totalCost) {
        this.totalCost = Float.parseFloat(totalCost);
    }

    public void setTotalCost(float totalCost) {
        this.totalCost = totalCost;
    }

    public float getTotalCost() {
        return totalCost;
    }

    public void setTelephone(String telephone) {
        this.telephone = telephone;
    }

    public String getTelephone() {
        return telephone;
    }

    public void setMail(String mail) {
        this.mail = mail;
    }

    public String getMail() {
        return mail;
    }

}