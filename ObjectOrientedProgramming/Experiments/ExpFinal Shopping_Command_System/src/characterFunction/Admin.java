package pers.Steven.shoppingManagementSystem.characterFunction;

import pers.Steven.shoppingManagementSystem.universalFunction.InputChecker;
import pers.Steven.shoppingManagementSystem.universalFunction.Item;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class Admin extends Person {
    private ArrayList<User> allUserData = new ArrayList<>();
    InputChecker inputChecker = new InputChecker();

    public Admin() {
        //循环5次的操作
        for (int i = 0; i < 5; i++) {
            loginState = login();
            if (getLoginState()) {
                break;
            } else {
                System.out.println("输入错误，您还有" + (4 - i) + "次机会");
            }
        }
        if (getLoginState()) {//登录成功，执行初始化
            initializeShopping();
            initializeAllUserData();
        }
    }

    //以下为管理员操作用户信息的方法
    //初始化所有的用户信息
    private void initializeAllUserData() {
        //获取获取所有用户的信息，然后执行User类的initialize方法完成初始化
        ArrayList<String> allUserData = getEveryLineMessageFromFile(USER_ACCOUNT_LIST_FILE);

        for (String thisUserData : allUserData) {
            String[] index = thisUserData.split("~");//获取到用户名和密码，并分开了
            User currUser = new User(index[0], index[1]);
            currUser.initializeUserMessage();
            this.allUserData.add(currUser);
        }
    }

    //显示所有的用户信息
    public int commandUser_showAllUserMessage() {
        int i = 0;
        for (; i < allUserData.size(); i++) {
            System.out.println("用户编号：" + (i + 1));
            allUserData.get(i).showAllMessage();
        }
        return allUserData.size();//返回到最后一个的序号，个数要在此基础上+1
    }

    //查找用户信息的功能，作为下一个操作的部分功能模块
    private ArrayList<Integer> searchUserData() {
        int searchKind;//记录查找种类
        String KeyWord;//查找关键词
        ArrayList<Integer> index = new ArrayList<>();//记录符合条件的商品在ArrayList里的index，作为返回值
        System.out.println("请选择您要查找的信息种类：");
        System.out.println("""
                1.用户名
                2.等级
                3.消费金额
                4.手机号码
                5.邮箱地址
                """);
        searchKind = inputChecker.checkSwitchRange(5);
        if (searchKind == 0) {
            searchUserData();
        }
        //获取查找关键词
        System.out.print("请输入查找关键词：");
        KeyWord = inputChecker.getInputString();
        switch (searchKind) {
            case 1 -> {
                for (int i = 0; i < allUserData.size(); i++) {
                    if (allUserData.get(i).getAccount().contains(KeyWord))
                        index.add(i);
                }
            }
            case 2 -> {
                for (int i = 0; i < allUserData.size(); i++) {
                    // 这个判定式的意思是若查找内容和level（数字）相同，或查找内容和等级称号部分符合即可
                    if (String.valueOf(allUserData.get(i).getLevel()).equals(KeyWord) || (allUserData.get(i).getLevel() == 0 ? ("铜牌客户") : (allUserData.get(i).getLevel() == 1 ? ("银牌客户") : ("金牌客户"))).contains(KeyWord))
                        index.add(i);
                }
            }
            case 3 -> {
                for (int i = 0; i < allUserData.size(); i++) {
                    if (String.valueOf(allUserData.get(i).getTotalCost()).equals(KeyWord))
                        index.add(i);
                }
            }
            case 4 -> {
                for (int i = 0; i < allUserData.size(); i++) {
                    if (allUserData.get(i).getTelephone().equals(KeyWord))
                        index.add(i);
                }
            }
            case 5 -> {
                for (int i = 0; i < allUserData.size(); i++) {
                    if (allUserData.get(i).getMail().equals(KeyWord))
                        index.add(i);
                }
            }
            default -> System.out.println("您的输入有误，请重试");
        }
        return index;
    }

    //查找用户信息
    public void commandUser_searchUserMessage() {
        ArrayList<Integer> index = searchUserData();
        for (int i : index) {
            System.out.println("用户序号：" + (i + 1));
            allUserData.get(i).showAllMessage();
        }
        System.out.println("即将返回主菜单\n");
    }

    //删除用户信息
    public void commandUser_removeUserMessage() {//要删除的包括：账号库中的账号、购物历史文件、购物车文件、个人账号文件
        int index, ID, userNum;//index是操作时的索引
        boolean accountPosition, curtPosition, historyPosition;
        userNum = commandUser_showAllUserMessage();
        System.out.print("请输入你想要删除的用户ID:");
        ID = inputChecker.checkSwitchRange(userNum);
        if (ID == 0) {
            commandUser_removeUserMessage();
        }

        index = ID - 1;
        System.out.print("您要删除的用户为：" + allUserData.get(index).getAccount());
        boolean confirmPosition = inputChecker.alertAndConfirm();
        if (confirmPosition) {
            //移除个人账号文件
            File accountMessage = getPersonalAccountMessageFile(allUserData.get(index).getAccount());
            accountPosition = accountMessage.delete();
            //移除购物车文件
            File accountCurtFile = getPersonalAccountCurtFile(allUserData.get(index).getAccount());
            curtPosition = accountCurtFile.delete();
            //移除购物历史
            File accountHistoryFile = getPersonalAccountHistoryFile(allUserData.get(index).getAccount());
            historyPosition = accountHistoryFile.delete();
            //移除账号库中的账号，及其在集合框架中的所有信息
            allUserData.remove(index);
            if (accountPosition && curtPosition && historyPosition) {
                System.out.println("删除完成，即将返回主菜单\n");
            } else {
                System.out.println("删除失败");
            }
        } else {
            System.out.println("删除操作已取消\n");
            commandUser_removeUserMessage();
        }
    }

    //重置用户密码
    public void commandUser_resetUserPassword() {
        int index, ID, userNum;
        String newPassword;
        userNum = commandUser_showAllUserMessage();
        System.out.println("请输入你想要重置密码的用户ID");

        ID = inputChecker.checkSwitchRange(userNum);
        index = ID - 1;
        if (ID == 0) {
            System.out.println("未找到该用户，即将返回上级菜单");
            return;
        }
        System.out.println("即将修改密码的用户为：" + allUserData.get(index).getAccount());
        boolean confirmPosition = inputChecker.alertAndConfirm();
        if (confirmPosition) {
            System.out.println("请输入新密码：");
            newPassword = inputChecker.getInputString();
            if (inputChecker.checkPasswordLegality(newPassword)) {
                allUserData.get(index).setPassword(newPassword);
            }
            System.out.println("修改完成");
        } else {
            System.out.println("您的输入有误，修改操作未执行，请重试");
            commandUser_resetUserPassword();
        }
    }

    //将用户信息改变保存到文件里
    public void commandUser_writeInFile() {
        FileWriter writeInFile;
        try {
            writeInFile = new FileWriter(USER_ACCOUNT_LIST_FILE);
            for (User thisUserData : allUserData) {
                writeInFile.write(thisUserData.getAccount() + "~" + thisUserData.getPassword() + "\n");
            }
            writeInFile.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //以下为管理员操作商品数据库信息的方法
    // 显示所有的商品信息
    public int commandItem_showAllItemMessage() {
        int itemNum = 0;
        for (int i = 0; i < MallItems.size(); i++) {
            System.out.println("商品序号：" + (i + 1));
            MallItems.get(i).showAllMessageForAdmin();
            itemNum++;
        }
        System.out.println("所有商品显示完毕，共" + MallItems.size() + "件，即将返回上级菜单");
        return itemNum;
    }

    //添加商品信息
    public void commandItem_addItemMessage() {
        Item newItem = new Item();

        System.out.println("--------开始商品信息录入--------");
        System.out.print("请输入商品名称：");
        newItem.setName(inputChecker.getInputString());
        System.out.print("请输入生产厂家：");
        newItem.setManufacturer(inputChecker.getInputString());
        System.out.print("请输入生产日期：（请按照年-月-日的格式输入）");
        newItem.setManuDate(inputChecker.getInputString());
        System.out.print("请输入型号：");
        newItem.setType(inputChecker.getInputString());
        System.out.print("请输入进货价：");
        newItem.setBuyingPrice(inputChecker.getInputString());
        System.out.print("请输入零售价：");
        newItem.setSellPrice(inputChecker.getInputString());
        System.out.print("请输入数量：");
        newItem.setNum(inputChecker.getInputString());
        MallItems.add(newItem);
        System.out.println("\n商品输入完成");
        MallItems.get(MallItems.size() - 1).showAllMessageForAdmin();
    }

    //查找商品信息
    public void commandItem_searchItemMessage() {
        System.out.println("""
                请选择查找类型：
                1.商品名称
                2.生产厂家
                3.生产日期
                4.型号
                5.售价
                """);
        int searchKind = inputChecker.checkSwitchRange(4);
        if (searchKind == 0) {
            commandItem_searchItemMessage();
        }
        System.out.print("请输入关键词（若是按照售价查询请使用正负数表示大于或小于）：");
        String keyword = inputChecker.getInputString();
        ArrayList<Integer> index = searchItemData(searchKind, keyword);
        if (index.size() != 0) {
            System.out.println("查询到以下结果：");
            for (int i : index) {
                MallItems.get(i).showAllMessageForAdmin();
            }
        } else {
            System.out.println("未查询到符合条件的商品");
        }
        System.out.println("即将返回主菜单");
    }

    //修改某商品信息
    public void commandItem_modifyItemMessage() {
        int ID, index, choice;//被修改的物品ID、选择被修改的项目
        String newMessage;
        int itemNum = commandItem_showAllItemMessage();
        System.out.print("请输入你想要修改的商品ID：");
        ID = inputChecker.checkSwitchRange(itemNum);
        if (ID == 0) {
            System.out.println("输入有误，已退出");
            commandItem_modifyItemMessage();
        }

        index = ID - 1;
        System.out.println("您要修改的商品为：");
        MallItems.get(index).showAllMessageForAdmin();

        System.out.println("""
                请选择您要修改的条目：
                \t1.商品名称
                \t2.生产厂家
                \t3.生产日期
                \t4.型号
                \t5.进货价
                \t6.零售价
                \t7.数量""");
        choice = inputChecker.checkSwitchRange(7);
        if (choice == 0) {
            System.out.println("您的输入有误，请重试");
            commandItem_modifyItemMessage();
        }

        System.out.println("请输入修改后的信息：");
        newMessage = inputChecker.getInputString();

        switch (choice) {
            case 1 -> {
                System.out.println("商品名称即将由“" + MallItems.get(index).getName() + "”修改为“" + newMessage + "“");
                MallItems.get(index).setName(newMessage);
            }
            case 2 -> {
                System.out.println("生产厂家即将由”" + MallItems.get(index).getManufacturer() + "“修改为”" + newMessage + "“");
                MallItems.get(index).setManufacturer(newMessage);
            }
            case 3 -> {
                System.out.println("生产日期即将由“" + MallItems.get(index).getManuDate() + "”修改为“" + newMessage + "“");
                MallItems.get(index).setManuDate(newMessage);
            }
            case 4 -> {
                System.out.println("型号即将由”" + MallItems.get(index).getType() + "“修改为”" + newMessage + "“");
                MallItems.get(index).setType(newMessage);
            }
            case 5 -> {
                System.out.println("进货价即将由“" + MallItems.get(index).getBuyingPrice() + "“修改为”" + newMessage + "“");
                MallItems.get(index).setBuyingPrice(newMessage);
            }
            case 6 -> {
                System.out.println("零售价即将由”" + MallItems.get(index).getSellPrice() + "”修改为“" + newMessage + "“");
                MallItems.get(index).setSellPrice(newMessage);
            }
            case 7 -> {
                System.out.println("数量即将由“" + MallItems.get(index).getNum() + "”修改为“" + newMessage + "“");
                MallItems.get(index).setNum(newMessage);
            }
            default -> {
                System.out.println("您的输入有误，请重试");
                commandItem_modifyItemMessage();
            }
        }
        System.out.println("您的修改执行完毕");
        System.out.println("新的商品信息如下：");
        MallItems.get(index).showAllMessageForAdmin();
        System.out.println("即将返回菜单");
    }

    //删除某商品信息
    public void commandItem_removeItemMessage() {
        int ID, index, itemNum;
        itemNum = commandItem_showAllItemMessage();

        System.out.print("请输入你想要删除的商品ID：");
        ID = inputChecker.checkSwitchRange(itemNum);
        if (ID == 0) {
            System.out.println("您的输入有误，请重试");
            commandItem_removeItemMessage();
        }
        index = ID - 1;
        System.out.print("即将删除的的商品为：");
        MallItems.get(index).showAllMessageForAdmin();
        System.err.println("请注意，商品删除后将无法复原");
        boolean confirmPosition = inputChecker.alertAndConfirm();
        if (confirmPosition) {
            MallItems.remove(ID - 1);
            System.out.println("删除完成");
        } else {
            System.out.println("您的输入有误，删除操作未执行，请重试");//直接返回上级菜单
        }
    }

    //将商品改变保存到文件里
    public void commandItem_writeInFile() {
        FileWriter writeInFile;
        try {
            writeInFile = new FileWriter(SHOPPING_ITEM_LIST_FILE);
            for (Item mallItem : MallItems) {
                writeInFile.write(mallItem.getWriteInString() + "\n");
            }
            writeInFile.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
