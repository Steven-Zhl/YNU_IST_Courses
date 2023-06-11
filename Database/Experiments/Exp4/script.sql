-- Active: 1663490780267@@127.0.0.1@3306@student_course

use student_course;

-- Ques 1

-- (1):嵌套查询：查询cno为2的学生

SELECT sname
from student
WHERE sno IN (
        SELECT sno
        from sc
        WHERE cno = '2'
    );

-- (2):嵌套查询：查找和张三同系的学生

SELECT sno, sname, sdept
FROM student
WHERE sdept = (
        SELECT sdept
        FROM student
        WHERE sname = '张三'
    );

-- (3):集合查询：查找计算机系学生及年龄不大于19岁的学生

-- 就是“计算机系”和“不大于19岁”两个群体的并集。

(
    SELECT *
    FROM student
    WHERE sdept = '计算机'
)
UNION (
    SELECT *
    FROM student
    WHERE sage <= 19
);

-- (4) 集合查询：查询计算机系和年龄不大于19岁学生的差集

-- 就是从“计算机系”学生中除去“年龄不大于19”岁的学生。MySQL中没有EXCEPT，所以只能用这种办法代替了

SELECT * FROM student WHERE sdept = '计算机' AND sage>19;

-- (5) 基于派生表的查询：找出每个学生超过他自己选修课平均成绩的课程号

SELECT sno, cno
FROM sc, (
        SELECT
            sno,
            AVG(grade)
        FROM sc
        GROUP BY (sno)
    ) AS Avg_sc(avg_sno, avg_score)
WHERE
    sc.sno = Avg_sc.avg_sno
    AND sc.grade > Avg_sc.avg_score;