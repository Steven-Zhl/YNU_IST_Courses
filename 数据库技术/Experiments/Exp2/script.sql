-- 1
-- 先创建一些测试项并查询
use student_course;
INSERT INTO student
SET
    sno = '20201060351',
    sname = 'Zhl',
    ssex = '男',
    sage = 20,
    sdept = '智能科学与技术';
INSERT INTO course
SET
    cno = 'cno_数据库',
    cname = '数据库技术',
    cpno = NULL,
    ccredit = 3;
INSERT INTO sc SET sno='20201060351', cno='cno_数据库', grade=3;
-- 删除这些信息
use student_course;
DELETE FROM sc;
DELETE FROM student;
DELETE FROM course;

-- 2
-- 按要求录入信息
use student_course;
INSERT INTO student
SET
    sno = '20191060001',
    sname = '张三',
    ssex = '男',
    sage = 20,
    sdept = '计算机';
INSERT INTO student
SET
    sno = '20191060002',
    sname = '李四',
    ssex = '女',
    sage = 19,
    sdept = '通信工程';
INSERT INTO student
SET
    sno = '20191060003',
    sname = '王五',
    ssex = '男',
    sage = 20,
    sdept = '计算机';
INSERT INTO student
SET
    sno = '20191060004',
    sname = '赵六',
    ssex = '男',
    sage = 19,
    sdept = '通信工程';
INSERT INTO student
SET
    sno = '20191060005',
    sname = '钱七',
    ssex = '女',
    sage = 18,
    sdept = '计算机';
INSERT INTO course SET cno='1',cname='C 语言',cpno=NULL,ccredit=3;
INSERT INTO course SET cno='2',cname='数据结构',cpno='1',ccredit=3;
INSERT INTO course SET cno='3',cname='数据库',cpno='2',ccredit=4;
INSERT INTO course SET cno='4',cname='操作系统',cpno='2',ccredit=4;
INSERT INTO course SET cno='5',cname='数据挖掘',cpno='3',ccredit=2;
INSERT INTO course SET cno='6',cname='人工智能',cpno='2',ccredit=2;
INSERT INTO sc SET sno='20191060001',cno='1',grade=68;
INSERT INTO sc SET sno='20191060001',cno='2',grade=76;
INSERT INTO sc SET sno='20191060001',cno='3',grade=80;
INSERT INTO sc SET sno='20191060002',cno='1',grade=77;
INSERT INTO sc SET sno='20191060002',cno='2',grade=80;
INSERT INTO sc SET sno='20191060002',cno='4',grade=85;
INSERT INTO sc SET sno='20191060003',cno='1',grade=90;
INSERT INTO sc SET sno='20191060003',cno='2',grade=92;
INSERT INTO sc SET sno='20191060003',cno='3',grade=90;
INSERT INTO sc SET sno='20191060003',cno='5',grade=91;
INSERT INTO sc SET sno='20191060004',cno='1',grade=88;
INSERT INTO sc SET sno='20191060004',cno='6',grade=90;
INSERT INTO sc SET sno='20191060005',cno='1',grade=86;
INSERT INTO sc SET sno='20191060005',cno='5',grade=88;

-- 3 更新数据
UPDATE student
SET sage = sage - 1
WHERE sdept = '计算机';

-- 4 修改数据
UPDATE sc
SET grade = grade + 5
WHERE cno = (
        SELECT cno
        FROM course
        WHERE cname = '数据库'
    );

-- 5
CREATE TABLE
    SC_cs(
        sno CHAR(11) NOT NULL,
        cno CHAR(11) NOT NULL,
        grade SMALLINT,
        PRIMARY KEY(sno, cno)
    );
-- 第一种
INSERT INTO sc_cs
SELECT SC.*
FROM SC
WHERE sno IN (
        SELECT sno
        FROM student
        WHERE sdept = '计算机'
    );
-- 第二种
INSERT INTO SC_cs
SELECT SC.*
FROM SC
    INNER JOIN student ON SC.sno = student.sno
WHERE sdept = '计算机';

-- 6
DELETE FROM sc
WHERE sno = (
        SELECT sno
        FROM student
        WHERE sname = '张三'
    );

-- 7
use world;
CREATE TABLE
    Country_Simple(
        Code CHAR(3) NOT NULL,
        Name CHAR(52) NOT NULL,
        Capital INT DEFAULT NULL,
        PRIMARY KEY(Code)
    );
INSERT INTO Country_Simple SELECT Code,Name,Capital FROM country;

-- 8
use world;
CREATE TABLE
    City_Simple(
        ID INT NOT NULL AUTO_INCREMENT,
        Name CHAR(35) NOT NULL,
        CountryCode CHAR(3) NOT NULL,
        PRIMARY KEY (ID)
    );
INSERT INTO City_Simple SELECT ID,Name,CountryCode FROM city;

-- 9
use world;
CREATE TABLE
    CL_Simple(
        CountryCode CHAR(3) NOT NULL,
        Language CHAR(30) NOT NULL,
        PRIMARY KEY (CountryCode, Language)
    );
INSERT INTO CL_Simple 10
SELECT CountryCode, Language
FROM countrylanguage;