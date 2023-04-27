package com.company;

public class Level {
    final private int levelNo;   //各级别号
    final private int strLength; //各级别一次输出字符串的长度
    final private int strTimes;  //各级别输出字符串的次数
    final private int timeLimit; //各级别闯关的时间限制
    final private int perScore;  //各级别正确输入一次的得分
    //用构造方法初始化这些常量
    Level(int levelNo, int strLength, int strTimes, int timeLimit, int perScore) {
        this.levelNo = levelNo;
        this.strLength = strLength;
        this.strTimes = strTimes;
        this.timeLimit = timeLimit;
        this.perScore = perScore;
    }

    public int showLevelNo() {
        return levelNo;
    }

    public int showStrLength() {
        return strLength;
    }

    public int showStrTimes() {
        return strTimes;
    }

    public int showTimeLimit() {
        return timeLimit;
    }

    public int showPerScore() {
        return perScore;
    }
}
