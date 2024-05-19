package com.company;

public class LevelParam {//此类对各个等级的各项属性进行初始化
    static Level[] levels = new Level[6];//创建6个level

    //可以说是新版初始化
    static {
        levels[0] = new Level(1, 2, 2, 30, 1);
        levels[1] = new Level(2, 3, 2, 26, 2);
        levels[2] = new Level(3, 4, 2, 22, 5);
        levels[3] = new Level(4, 5, 2, 18, 8);
        levels[4] = new Level(5, 6, 2, 15, 10);
        levels[5] = new Level(6, 7, 2, 12, 15);
    }

    int getStrLength(int level) {
        return levels[level - 1].showStrLength();
    }

    int getTimeLimit(int level) {
        return levels[level - 1].showTimeLimit();
    }

    int getStrTimes(int level) {
        return levels[level - 1].showStrTimes();
    }

    int getPerScore(int level) {
        return levels[level - 1].showPerScore();
    }

    int getMaxLevel() {
        return levels[levels.length - 1].showLevelNo();
    }
}