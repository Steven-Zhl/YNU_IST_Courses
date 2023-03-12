-- 用于批量向student_course库中的三个表批量添加测试数据
CREATE PROCEDURE `batch_insert_student`()
BEGIN
    DECLARE i INT;
    SET i = 1;
    WHILE i <= 1000
        DO
            INSERT INTO student
            SET sno  =concat(20191060005 + i),
                sname=concat('学生', i),
                ssex=if(i % 2 = 0, '男', '女'),
                sage=if(i % 2 = 0, 20, 21),
                sdept='计算机科学与技术';
            SET i = i + 1;
        end while;
END;

CREATE PROCEDURE `batch_insert_course`()
BEGIN
    DECLARE i INT;
    SET i = 7;
    WHILE i <= 100
        DO
            INSERT INTO course
            SET cno=concat(i),
                cname= concat('课程', i - 6),
                cpno=concat(i - 6),
                ccredit=if(i % 2 = 0, 2, 3);
            SET i = i + 1;
        END WHILE;
END;

CREATE PROCEDURE `batch_insert_sc`()
BEGIN
    DECLARE i INT;
    DECLARE j INT;
    SET i = 1;
    WHILE i <= 1000
        DO
            SET j = 1;
            WHILE j <= 10
                DO
                    INSERT INTO sc
                    SET sno=concat(20191060005 + i),
                        cno=concat(j),
                        grade=if(i % 2 = 0, 60, 70);
                    SET j = j + 1;
                END WHILE;
            SET i = i + 1;
        END WHILE;
END;

call batch_insert_student();
call batch_insert_course();
call batch_insert_sc();

-- 题1：
-- 无索引单表查询
SELECT * FROM student WHERE sname = '学生233';
-- 主码索引单表查询
SELECT * FROM student WHERE sno = '20191060233';
-- 无索引连接查询
SELECT * FROM student, sc WHERE student.sno = sc.sno AND student.sname = '学生233';
-- 主码索引连接查询
SELECT * FROM student, sc WHERE student.sno = sc.sno AND student.sno = '20191060233';
-- 无索引子查询
SELECT * FROM student WHERE sname = (SELECT sname FROM student WHERE sno = '20191060233');

-- 题2：
-- 无索引单表查询
SELECT * FROM customer WHERE nationkey <= 200;
-- 主码索引单表查询
SELECT * FROM nation WHERE nationkey = 100;
-- 无索引连接查询
SELECT * FROM supplier, nation;
-- 主码索引连接查询
SELECT * FROM customer, orders 
  WHERE customer.custkey = orders.custkey 
        AND orders.orderkdy <= 100;
-- 嵌套子查询
SELECT * FROM customer WHERE nationkey in (
    SELECT nationkey FROM nation WHERE regionkey = (
        SELECT regionkey FROM region WHERE name = '亚洲'));