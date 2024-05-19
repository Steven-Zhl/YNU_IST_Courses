package pers.Steven.shoppingManagementSystem.characterFunction;

import pers.Steven.shoppingManagementSystem.universalFunction.InputChecker;
import pers.Steven.shoppingManagementSystem.universalFunction.Item;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.security.MessageDigest;
import java.util.ArrayList;

public abstract class Person {
    String account, password;
    boolean loginState = false;
    ArrayList<Item> MallItems = new ArrayList<>();//存储商店内容
    //几个路径常量
    static final File SHOPPING_ITEM_LIST_FILE = new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\ItemsFactory");
    static final File ADMIN_ACCOUNT_LIST_FILE = new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\AccountMessage\\AdminAccounts.txt");
    static final File USER_ACCOUNT_LIST_FILE = new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\AccountMessage\\UserAccounts.txt");
    InputChecker inputChecker = new InputChecker();

    //登录
    boolean login() {
        String inputAccount, inputPassword;//用户输入的账号密码
        //获取输入信息
        System.out.print("请输入账号：");
        inputAccount = inputChecker.getInputString();
        System.out.print("请输入密码：");
        inputPassword = inputChecker.getInputString();
        inputPassword=getMD5String(inputPassword);
        //检测是否可以登录，以及用户登录成功后向当前对象内初始化
        ArrayList<String> accountList = null;
        if (this instanceof User) {//设置文件指向
            accountList = getEveryLineMessageFromFile(USER_ACCOUNT_LIST_FILE);
        } else if (this instanceof Admin) {
            accountList = getEveryLineMessageFromFile(ADMIN_ACCOUNT_LIST_FILE);
        }

        String checkedString = inputAccount + "~" + inputPassword;//格式化被查找的字符串
        for (String thisLineAccount : accountList) {
            if (checkedString.equals(thisLineAccount)) {//说明存在该账户，登录完成，向当前对象写入属性
                password = inputPassword;
                account = inputAccount;
                return true;
            }
        }
        //说明登录失败了
        account = null;
        password = null;
        return false;
    }

    //修改个人密码
    public boolean changePassword() {
        File accountFile = null;
        String inputOriginalPassword, inputNewPassword;
        String originAccount = this.getAccount(), originPassword = this.getPassword();//记录原密码和新密码以进行比对

        //获取必要信息
        System.out.print("请输入原密码：");
        inputOriginalPassword = inputChecker.getInputString();
        inputOriginalPassword=getMD5String(inputOriginalPassword);
        if (!inputOriginalPassword.equals(originPassword)) {
            System.out.println("原密码输入错误！");
            return false;
        }
        System.out.print("请输入新密码：");
        inputNewPassword = inputChecker.getInputString();
        if (!inputChecker.checkPasswordLegality(inputNewPassword)) {
            System.out.println("您的新密码不合法，请使用大小写字母、数字和标点符号的组合，且长度不低于8位的字符串作为新密码");
            return false;
        }

        //现在已经确认身份了，可以修改密码了。根据身份不同，对 accountFile的指向进行修改，先获取到所有的账号名单
        inputNewPassword=getMD5String(inputNewPassword);//加密
        if (this instanceof Admin) {
            accountFile = ADMIN_ACCOUNT_LIST_FILE;
        } else if (this instanceof User) {
            accountFile = USER_ACCOUNT_LIST_FILE;
        }
        ArrayList<String> accountList = getEveryLineMessageFromFile(accountFile);
        //找到要修改的那个账号，并修改
        for (int i = 0; i < accountList.size(); i++) {
            String thisAccount = accountList.get(i).split("~")[0];
            if (originAccount.equals(thisAccount)) {//找到了账号
                accountList.set(i, originAccount + "~" + inputNewPassword);
            }
        }
        //将其写入文件
        boolean writeState = writeInFile(accountList, accountFile);
        if (writeState) {
            return true;
        } else {
            System.out.println("未完成注册");
            return false;
        }
    }

    //修改他人密码（适合管理员以及找回密码时使用）
    public boolean changePassword(String account, String newPassword) {
        File accountFile;

        if (!inputChecker.checkPasswordLegality(newPassword)) {
            System.out.println("您的新密码不合法，请使用大小写字母、数字和标点符号的组合，且长度不低于8位的字符串作为新密码");
            return false;
        }

        //现在已经确认身份了，可以修改密码了。先获取到所有的账号名单
        accountFile = USER_ACCOUNT_LIST_FILE;
        ArrayList<String> accountList = getEveryLineMessageFromFile(accountFile);

        //找到要修改的那个账号，并修改
        for (int i = 0; i < accountList.size(); i++) {
            String[] thisAccount = accountList.get(i).split("~");//将原字符串通过分隔符分成两段，第一段是账号
            if (account.equals(thisAccount[0])) {//比较
                newPassword=getMD5String(newPassword);
                accountList.set(i, account + "~" + newPassword);
                break;
            }
        }

        //将其写入文件
        boolean writeState = writeInFile(accountList, accountFile);
        if (writeState) {
            return true;
        } else {
            System.out.println("未完成修改密码");
            return false;
        }
    }

    //商城的初始化
    public void initializeShopping() {
        ArrayList<String> itemList = getEveryLineMessageFromFile(SHOPPING_ITEM_LIST_FILE); //获取到每一行的商品信息
        for (String s : itemList) {
            Item itemPointer = new Item(s);//这将会根据商品存入字符串拆成属性，对该商品进行初始化
            MallItems.add(itemPointer);
        }
    }

    //通过产品名找序号，未找到返回-1
    public int searchItemIndexByName(String name) {
        for (int i = 0; i < MallItems.size(); i++) {
            if (MallItems.get(i).getName().equals(name))
                return i;
        }
        return -1;
    }

    //查找并返回符合条件的下标组
    ArrayList<Integer> searchItemData(int findKind, String keyWord) {
        final int ITEM_NAME = 1, ITEM_MANUFACTURER = 2, ITEM_MANUFACTURE_DATE = 3, ITEM_TYPE = 4, ITEM_PRICE = 5;//依次对应 1.商品名称2.生产厂家3.生产日期、4.型号
        ArrayList<Integer> index = new ArrayList<>();//记录符合条件的商品在ArrayList里的index，作为返回值

        switch (findKind) {
            case ITEM_NAME -> {
                for (int i = 0; i < MallItems.size(); i++) {
                    if (MallItems.get(i).getName().contains(keyWord))
                        index.add(i);
                }
            }
            case ITEM_MANUFACTURER -> {
                for (int i = 0; i < MallItems.size(); i++) {
                    if (MallItems.get(i).getManufacturer().contains(keyWord))
                        index.add(i);
                }
            }
            case ITEM_MANUFACTURE_DATE -> {
                for (int i = 0; i < MallItems.size(); i++) {
                    if (MallItems.get(i).getManuDate().contains(keyWord))
                        index.add(i);
                }
            }
            case ITEM_TYPE -> {
                for (int i = 0; i < MallItems.size(); i++) {
                    if (MallItems.get(i).getType().contains(keyWord))
                        index.add(i);
                }
            }
            case ITEM_PRICE -> {
                int price = Integer.parseInt(keyWord);
                if (price > 0) {
                    for (int i = 0; i < MallItems.size(); i++) {
                        if (MallItems.get(i).getSellPrice() >= Math.abs(price))
                            index.add(i);
                    }
                } else if (price < 0) {
                    for (int i = 0; i < MallItems.size(); i++) {
                        if (MallItems.get(i).getSellPrice() <= Math.abs(price))
                            index.add(i);
                    }
                } else if (price == 0) {
                    for (int i = 0; i < MallItems.size(); i++) {
                        if (MallItems.get(i).getSellPrice() == 0)
                            index.add(i);
                    }
                }
            }
            default -> System.out.println("您的输入有误，请重试");//当然正常来说是不会到这一步的
        }
        return index;
    }

    //账户相关的get与set
    public String getAccount() {
        return account;
    }

    public boolean getLoginState() {
        return loginState;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    //获取个人账户信息路径（不包括购物历史）
    public File getPersonalAccountMessageFile() {
        return new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\UserMessage\\" + getAccount() + ".txt");
    }

    public File getPersonalAccountMessageFile(String account) {
        return new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\UserMessage\\" + account + ".txt");
    }

    //获取个人账户购物历史路径
    public File getPersonalAccountHistoryFile() {
        return new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\UserShoppingHistory\\" + getAccount() + ".txt");
    }

    public File getPersonalAccountHistoryFile(String account) {
        return new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\UserShoppingHistory\\" + account + ".txt");
    }

    //获取个人账户购物车路径
    public File getPersonalAccountCurtFile() {
        return new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\UserCurt\\" + getAccount() + ".txt");
    }

    public File getPersonalAccountCurtFile(String account) {
        return new File("C:\\Users\\张翰林\\IdeaProjects\\Shopping Command System\\src\\Personal\\ProgramDesign\\Storage\\UserCurt\\" + account + ".txt");
    }

    // 从某个文件中读取所有内容（不改变格式）
    public ArrayList<String> getEveryLineMessageFromFile(File filePath) {
        File path = filePath;
        ArrayList<String> returnContents = new ArrayList<>();
        try {
            FileReader file = new FileReader(path);
            BufferedReader readFile = new BufferedReader(file);
            String thisLineMessage = readFile.readLine();
            while (thisLineMessage != null) {
                returnContents.add(thisLineMessage);
                thisLineMessage = readFile.readLine();
            }
            readFile.close();
            file.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return returnContents;
    }

    // 向某个文件中写入所有内容（原生格式，覆写原文，若是仅需添加某项不可用）
    public boolean writeInFile(ArrayList<String> inputContents, File filePath) {
        File path = filePath;
        try {
            FileWriter file = new FileWriter(path);
            BufferedWriter writeFile = new BufferedWriter(file);
            for (String thisMessage : inputContents) {
                writeFile.write(thisMessage + "\n");
            }
            writeFile.close();
            file.close();
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }

    public String getMD5String(String str) {
        try {
            // 生成一个MD5加密计算摘要
            MessageDigest md = MessageDigest.getInstance("MD5");
            // 计算md5函数
            md.update(str.getBytes());
            // digest()最后确定返回md5 hash值，返回值为8位字符串。因为md5 hash值是16位的hex值，实际上就是8位的字符
            // BigInteger函数则将8位的字符串转换成16位hex值，用字符串来表示；得到字符串形式的hash值
            //一个byte是八位二进制，也就是2位十六进制字符（2的8次方等于16的2次方）
            return new BigInteger(1, md.digest()).toString(16);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}