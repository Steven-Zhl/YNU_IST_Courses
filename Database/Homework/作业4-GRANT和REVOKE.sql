-- Ques7

CREATE TABLE
    部门 (
        部门号 CHAR(4) PRIMARY KEY,
        名称 VARCHAR(10) NOT NULL,
        经理名 CHAR(4) NOT NULL,
        地址 VARCHAR(20) NOT NULL,
        电话号 CHAR(11) NOT NULL,
        FOREIGN KEY (经理名) REFERENCES 员工(员工号)
    );

CREATE TABLE
    职工 (
        职工号 CHAR(6) PRIMARY KEY,
        姓名 CHAR(10) NOT NULL,
        年龄 INT NOT NULL,
        职务 CHAR(10) NOT NULL,
        工资 INT NOT NULL,
        部门号 CHAR(4) NOT NULL,
        FOREIGN KEY (部门号) REFERENCES 部门(部门号)
    );

-- 1

GRANT SELECT ON TABLE 职工, 部门 TO 王明;

-- 2

GRANT INSERT, DELETE ON TABLE 职工, 部门 TO 李勇;

-- 3

GRANT SELECT ON TABLE 职工 WHEN USER()= NAME TO ALL;

-- 4

GRANT SELECT, UPDATE(工资) ON TABLE 职工 TO 刘星;

-- 5

GRANT ALTER TABLE ON TABLE 职工, 部门 TO 张新;

-- 6

GRANT ALL ON TABLE 职工, 部门 TO 周平 WITH GRANT OPTION;

-- 7

CREATE VIEW 部分工资信息 AS 
	SELECT
	    部门.名称,
	    MAX(工资) AS 最高工资,
	    MIN(工资) AS 最低工资,
	    AVG(工资) AS 平均工资
	FROM 部门, 职工
	WHERE 部门.部门号 = 职工.部门号
	GROUP BY(部门.名称);
; 

GRANT SELECT ON TABLE 部分工资信息 TO 杨兰;

-- Ques8

-- 1

REVOKE SELECT ON TABLE 职工, 部门 FROM 王明;

-- 2

REVOKE INSERT, DELETE ON TABLE 职工, 部门 FROM 李勇;

-- 3

REVOKE SELECT ON TABLE 职工 WHEN USER()= NAME FROM ALL;

-- 4

REVOKE SELECT, UPDATE ON TABLE 职工 FROM 刘星;

-- 5

REVOKE ALTER TABLE ON TABLE 职工, 部门 FROM 张新;

-- 6

REVOKE ALL ON TABLE 职工, 部门 FROM 周平;

-- 7

REVOKE SELECT ON TABLE 部分工资信息 FROM 杨兰;