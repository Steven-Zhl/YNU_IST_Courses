package com.company;

public class User {
    String name;
    static int score = 0;
    int fistNumber;
    String fist;

    String showFist(int parameter) {
        fistNumber = parameter;
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
