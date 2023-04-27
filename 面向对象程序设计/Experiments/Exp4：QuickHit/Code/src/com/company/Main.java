package com.company;

public class Main {
//设计中，所有的get方法都是为了解决获取一个数据
    public static void main(String[] args) {
        Game game = new Game();
        while (true) {
            game.printStr();
            game.printResult();
        }
    }
}
