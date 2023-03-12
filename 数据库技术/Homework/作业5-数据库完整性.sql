-- Ques6

CREATE TABLE
    部门 (
        部门号 CHAR(4) PRIMARY KEY,
        名称 VARCHAR(10) NOT NULL,
        经理名 CHAR(4) NOT NULL,
        电话 CHAR(11) NOT NULL,
        FOREIGN KEY (经理名) REFERENCES 员工(员工号)
    );

CREATE TABLE
    职工 (
        职工号 CHAR(6) PRIMARY KEY,
        姓名 CHAR(10) NOT NULL,
        年龄 INT NOT NULL CHECK (年龄 <= 60),
        职务 CHAR(10) NOT NULL,
        工资 INT NOT NULL,
        部门号 CHAR(4) NOT NULL,
        FOREIGN KEY (部门号) REFERENCES 部门(部门号)
    );