package pers.Steven.shoppingManagementSystem;

import pers.Steven.shoppingManagementSystem.universalFunction.OperatorPage;

public class Main {
    /*
    设计规约:
    0. 最终目标是在大多数人都能看懂的情况下尽量做到系统性、整洁性
    1. SystemBase中每个分支都要做形成闭环，即具体的操作完成之后要完成回到菜单这一动作
    2. 提高模块化程度，应使用更多的常量作为标识
    3. 对于逻辑上类似的代码应尽量做到封装成方法，提高复用程度
    4. 所有异常都用try-catch包装，不添加到方法签名
    5. 商品和角色ID仅仅是用来操作的，全部用ArrayList的序列代替
    */
    public static void main(String[] args) {
        OperatorPage system = new OperatorPage();
    }
}