package pers.Steven.shoppingManagementSystem.universalFunction;

import pers.Steven.shoppingManagementSystem.characterFunction.Admin;
import pers.Steven.shoppingManagementSystem.characterFunction.Person;
import pers.Steven.shoppingManagementSystem.characterFunction.User;

import java.util.ArrayList;

public class OperatorPage {
    // show方法显示各种菜单与提示，与之同名的switch方法进行不同方法的分支
    Person person;//创建当前操作者的实例，实例化在之后
    private final int IDENTITY_USER = 1, IDENTITY_ADMIN = 2, IDENTITY_EXIT = 3;// 身份标识常量
    private int identity;// 和上面的几个常量对应
    InputChecker inputChecker = new InputChecker();

    //构造方法
    public OperatorPage() {
        showWelcomePage();
    }

    //该方法显示欢迎界面，并显示身份选择界面
    private void showWelcomePage() {
        System.out.println("""
                                
                ___       __        __                                    __      \s
                __ |     / /_______/ /__________________ ________      __/ /______\s        __   __ _________\s
                __ | /| / /_  _ \\_/ /_  ___/  __ \\_  __ `__ \\  _ \\    /__  __/  __ \\      / /  / /_  ___/  _ \\
                __ |/ |/ / /  __/  / / /__ / /_/ /  / / / / /  __/     / /_ / /_/ /      / /_/ /_(__  )/  __/
                ____/|__/  \\___//_/  \\___/ \\____//_/ /_/ /_/\\___/      \\__/ \\____/\s      \\__,_/ /____/ \\___/\s
                                
                                
                _____________                       _____               \s       ______                                                __
                __  ___/__  /__________________________(_)_____________ _     /  ____/____________ __________ _________ _____________/ /
                _____ \\__  __ \\  __ \\__  __ \\__  __ \\_  /__  __ \\_  __ `/    /  /    _  __ \\_  __ `__ \\_  __ `__ \\  __ `/_  __ \\  __  /\s
                ____/ /_  / / / /_/ /_  /_/ /_  /_/ /  / _  / / /  /_/ /\s   /  /___ /  /_/ /  / / / / /  / / / / / /_/ /_  / / / /_/ / \s
                /____/ /_/ /_/\\____/_  .___/_  .___//_/  /_/ /_/_\\__, / \s   \\_____/ \\____//_/ /_/ /_//_/ /_/ /_/ \\__,_/ /_/ /_/\\__,_/  \s
                                    /_/     /_/                 /____/  \s                                                                          \s
                               
                               
                ________                 __                \s
                __  ___/____  __________/ /____________ ___\s
                _____ \\__  / / /_  ___/  __/  _ \\_  __ `__ \\
                ____/ /_  /_/ /_(__  )/ /_ /  __/  / / / / /
                /____/ _\\__, / /____/ \\__/ \\___//_/ /_/ /_/\s
                       /____/                              \s
                请选择你的身份：
                \t1.用户
                \t2.管理员
                \t3.退出系统
                """);
        switchIdentity();
    }

    //获取身份
    private void switchIdentity() {
        identity = inputChecker.checkSwitchRange(3);
        switch (identity) {
            case IDENTITY_USER, IDENTITY_ADMIN -> showAccountActivity();
            case IDENTITY_EXIT -> {
                System.out.println("系统即将退出，感谢使用！");
                System.exit(0);
            }
            default -> {
                identity = 0;// 撤销身份设定
                showWelcomePage();
            }
        }
    }

    //显示确定身份后可执行的操作，包括登录、注册、退出、找回密码等
    private void showAccountActivity() {
        if (identity == IDENTITY_USER) {
            System.out.println("""
                    请选择：
                    \t1.登录
                    \t2.注册
                    \t3.找回密码
                    \t4.退出系统
                    """);
        } else if (identity == IDENTITY_ADMIN) {
            System.out.println("""
                    请选择：
                    \t1.登录
                    \t2.退出系统
                    """);
        }
        switchAccountActivity();
    }

    private void switchAccountActivity() {
        int function;
        if (identity == IDENTITY_USER) {
            final int FUNCTION_LOGIN = 1, FUNCTION_REGISTER = 2, FUNCTION_FINDPASSWORD = 3, FUNCTION_EXIT = 4;
            InputChecker inputChecker = new InputChecker();
            function = inputChecker.checkSwitchRange(4);
            switch (function) {
                case FUNCTION_LOGIN -> {
                    person = new User("登录");
                    if (person.getLoginState()) {
                        System.out.println("登录成功，欢迎使用");
                        showMenu();
                    } else {
                        System.out.println("即将返回菜单");
                        showAccountActivity();
                    }
                }
                case FUNCTION_REGISTER -> {
                    person = new User("注册");
                    showAccountActivity();
                }
                case FUNCTION_FINDPASSWORD -> {
                    person = new User("找回密码");
                    showAccountActivity();
                }
                case FUNCTION_EXIT -> {
                    System.out.println("您已退出系统，感谢使用");
                    System.exit(0);
                }
            }
        } else if (identity == IDENTITY_ADMIN) {
            final int FUNCTION_LOGIN = 1, FUNCTION_EXIT = 2;
            InputChecker inputChecker = new InputChecker();
            function = inputChecker.checkSwitchRange(2);
            switch (function) {
                case FUNCTION_LOGIN -> {
                    person = new Admin();
                    if (person.getLoginState())
                        showMenu();
                    else {
                        System.out.println("登录失败");
                        showAccountActivity();
                    }
                }
                case FUNCTION_EXIT -> {
                    System.out.println("您已退出系统，感谢使用");
                    System.exit(0);
                }
            }
        }
    }

    // 显示管理员或用户登录后的一级菜单
    private void showMenu() {
        int choice;
        if (person instanceof User) {//显示用户菜单
            System.out.println("------------菜-单------------");
            System.out.println("当前身份：用户\t\t用户名：" + person.getAccount());
            System.out.println("""
                    1.修改密码
                    2.进入购物系统
                    3.查看个人信息
                    4.退出登录
                    """);
        } else if (person instanceof Admin) {//显示管理员菜单
            System.out.println("------------菜-单------------");
            System.out.println("当前身份：管理员\t\t用户名：" + person.getAccount());
            System.out.println("""
                    1.修改密码
                    2.客户管理
                    3.商品管理
                    4.退出登录
                    """);
        }
        System.out.print("请选择功能：");
        choice = inputChecker.checkSwitchRange(4);
        if (choice == 0) {
            showMenu();
        }
        switchMenu(choice);
    }

    // 操作选项分支
    private void switchMenu(int choice) {
        if (person instanceof User) {
            switch (choice) {
                case 1 -> {
                    System.out.println("修改密码");
                    boolean changePasswordSituation = person.changePassword();
                    if (changePasswordSituation) {
                        System.out.println("修改成功，请重新登录");
                        System.exit(0);
                    } else {
                        System.out.println("修改失败");
                    }
                }
                case 2 -> {
                    System.out.println("进入购物系统");
                    showUserShoppingSystem();
                }
                case 3 -> {
                    System.out.println("查看个人信息");
                    ((User) person).showAllMessage();
                    System.out.println("显示完毕，即将返回主界面");
                    showMenu();
                }
                case 4 -> {
                    System.out.println("退出登录");
                    ArrayList<String> accountMessage = new ArrayList<>();
                    accountMessage.add(((User) person).getAccountWriteInString());
                    person.writeInFile(accountMessage, person.getPersonalAccountMessageFile());
                    System.out.println("即将退出系统，感谢使用！");
                }
                default -> {
                    System.out.println("您的输入有误，请重试！");
                    showMenu();
                }
            }
        } else if (person instanceof Admin) {
            switch (choice) {
                case 1 -> {
                    System.out.println("修改密码");
                    boolean changePasswordSituation = person.changePassword();
                    if (changePasswordSituation) {
                        System.out.println("修改成功，请重新登录");
                        System.exit(0);
                    } else {
                        System.out.println("修改失败");
                    }
                }
                case 2 -> {
                    System.out.println("客户管理");
                    showAdminCommandUserMenu();
                }
                case 3 -> {
                    System.out.println("商品管理");
                    showAdminCommandItemMenu();
                }
                case 4 -> {
                    System.out.println("退出登录");
                    System.out.println("账号即将退出，感谢您的使用");
                    System.exit(0);
                }
                default -> {
                    System.out.println("您的输入有误，请重试！");
                    showMenu();
                }
            }
        }
    }

    //显示管理员界面：商品管理子页面
    private void showAdminCommandItemMenu() {
        int chooseFunction;
        System.out.println("----------商-品-管-理----------");
        System.out.println("""
                \t1.显示所有商品信息
                \t2.添加商品信息
                \t3.修改商品信息
                \t4.删除商品信息
                \t5.查询商品信息
                \t6.返回上级菜单
                """);
        System.out.print("请选择功能：");
        chooseFunction = inputChecker.checkSwitchRange(6);
        if (chooseFunction == 0) {
            System.out.println("您的输入有误，请重试！");
            showAdminCommandItemMenu();
        }
        switchAdminCommandItemMenu(chooseFunction);
    }

    //管理员界面：商品管理子页面
    private void switchAdminCommandItemMenu(int choice) {
        //在返回上级菜单的时候将把ArrayList的内容写入文件，即更新
        switch (choice) {
            case 1 -> {//显示所有商品信息
                ((Admin) person).commandItem_showAllItemMessage();
                showAdminCommandItemMenu();
            }
            case 2 -> {//添加商品信息
                ((Admin) person).commandItem_addItemMessage();
                showAdminCommandItemMenu();
            }
            case 3 -> {//修改商品信息
                ((Admin) person).commandItem_modifyItemMessage();
                showAdminCommandItemMenu();
            }
            case 4 -> {//删除商品信息
                ((Admin) person).commandItem_removeItemMessage();
                showAdminCommandItemMenu();
            }
            case 5 -> {//查询商品信息
                ((Admin) person).commandItem_searchItemMessage();
                showAdminCommandItemMenu();
            }
            case 6 -> {//返回上级菜单（执行商品信息写入）
                ((Admin) person).commandItem_writeInFile();
                showMenu();
            }
            default -> {
                System.out.println("您的输入有误，请重试！");
                showAdminCommandItemMenu();
            }
        }
    }

    //显示管理员界面：客户管理子页面
    public void showAdminCommandUserMenu() {
        System.out.println("----------客-户-管-理----------");
        System.out.println("""
                \t1.显示所有客户信息
                \t2.查询客户信息
                \t3.删除客户信息
                \t4.重置用户密码
                \t5.返回上级菜单
                """);
        System.out.print("请选择功能：");
        int choice = inputChecker.checkSwitchRange(5);
        if (choice == 0) {
            showAdminCommandUserMenu();
        }
        switchAdminCommandUserMenu(choice);
    }

    //管理员界面：客户管理子页面(修改用户密码待测试)
    private void switchAdminCommandUserMenu(int choice) {
        switch (choice) {
            case 1 -> {//显示所有客户信息
                ((Admin) person).commandUser_showAllUserMessage();
                showAdminCommandUserMenu();
            }
            case 2 -> {//查询客户信息
                ((Admin) person).commandUser_searchUserMessage();
                showAdminCommandUserMenu();
            }
            case 3 -> {//删除客户信息
                ((Admin) person).commandUser_removeUserMessage();
                showAdminCommandUserMenu();
            }
            case 4 -> {//重置用户密码
                ((Admin) person).commandUser_resetUserPassword();
                showAdminCommandUserMenu();
            }
            case 5 -> {//返回上级菜单（执行个人信息写入）
                ((Admin) person).commandUser_writeInFile();
                showMenu();
            }
            default -> {
                System.out.println("您的输入有误，请重试！");
                showAdminCommandUserMenu();
            }
        }
    }

    //用户二级界面：购物系统
    private void showUserShoppingSystem() {
        System.out.println("----------购-物-管-理----------");
        System.out.println("""
                \t1.显示购物车
                \t2.添加商品至购物车
                \t3.移除购物车商品
                \t4.修改购物车商品数量
                \t5.结账
                \t6.查看购物历史
                \t7.退出购物系统
                """);
        System.out.print("请选择功能：");
        int choice = inputChecker.checkSwitchRange(7);
        if (choice == 0) {
            showUserShoppingSystem();
        }
        switchUserShoppingSystem(choice);
    }

    private void switchUserShoppingSystem(int choice) {
        switch (choice) {
            case 1 -> {
                System.out.println("显示购物车");
                ((User) person).showAllItemInCurt();
                showUserShoppingSystem();
            }
            case 2 -> {
                System.out.println("添加商品到购物车");
                ((User) person).addItemToCurt();
                showUserShoppingSystem();
            }
            case 3 -> {
                System.out.println("移除购物车商品");
                ((User) person).removeItemInCurt();
                showUserShoppingSystem();
            }
            case 4 -> {
                System.out.println("删减购物车商品数量");
                ((User) person).decreaseItemNumInCurt();
                showUserShoppingSystem();
            }
            case 5 -> {
                System.out.println("结账");
                ((User) person).payForCurt();
                showUserShoppingSystem();
            }
            case 6 -> {
                System.out.println("查看购物历史");
                ((User) person).showTheHistoryOfShopping();
                showUserShoppingSystem();
            }
            case 7 -> {
                System.out.println("退出购物系统");
                ((User) person).exitMenu();
                showMenu();
            }
        }
    }
}