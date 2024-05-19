package com.company;

public class Computer {
    String name;
    static int score = 0;
    int fistNumber;

    String showFist() {
        String fist=null;
        fistNumber = 1 + (int) (Math.random() * 3);
        if (fistNumber == 1) {
            fist = "剪刀";
        } else if (fistNumber == 2) {
            fist = "石头";
        } else if (fistNumber == 3) {
            fist = "布";
        }
        return fist;
    }
}
