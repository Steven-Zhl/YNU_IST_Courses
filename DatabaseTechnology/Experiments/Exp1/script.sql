-- 2(1)构建数据库

CREATE DATABASE Student_Course;

-- 创建Student_Course库

use Student_Course;

-- 选中Student_Course库

CREATE TABLE
    Student(
        sno CHAR(11) PRIMARY KEY,
        sname CHAR(10) NOT NULL,
        ssex CHAR(2),
        sage SMALLINT(2),
        sdept CHAR(20)
    );

-- 创建Student Table

CREATE TABLE
    Course(
        cno CHAR(11),
        cname CHAR(20) NOT NULL,
        cpno CHAR(11),
        ccredit SMALLINT(2) NOT NULL,
        PRIMARY KEY(cno),
        FOREIGN KEY(cpno) REFERENCES Course(cno)
    );

-- 创建Course Table

CREATE TABLE
    SC(
        sno CHAR(11),
        cno CHAR(11),
        grade SMALLINT(3),
        PRIMARY KEY(sno, cno),
        FOREIGN KEY(sno) REFERENCES Student(sno),
        FOREIGN KEY(cno) REFERENCES Course(cno)
    );

-- 创建SC Table

-- 2(2) 输入数据并测试实体完整性和参照完整性

INSERT INTO
    student(sno, sname, ssex, sage, sdept)
VALUES (
        20201060351,
        "testName",
        "男",
        18,
        "计算机科学与技术"
    );

INSERT INTO
    course(cno, cname, cpno, ccredit)
VALUES (
        '3011140073',
        '数据库技术',
        '3011140073',
        3
    );

-- 插入课程信息

INSERT INTO
    sc(sno, cno, grade)
VALUES (20201060351, '3011140073', 3);

-- 插入选课信息

DELETE FROM student WHERE sno='20201060351';

-- 测试