-- Active: 1667103467746@@127.0.0.1@3306@tpc_h

use student_course;

-- 一、验证课本例

-- 1 建立计算机系的学生信息视图

CREATE VIEW CS_STU AS 
	SELECT Sno, Sname, Sage
	FROM Student
	WHERE Sdept = '计算机'
	WITH CHECK
OPTION; 

-- 也可以这么写

CREATE VIEW CS_STU_2(SNO, SNAME, SAGE) AS 
	SELECT student.Sno, Sname, Sage FROM student WHERE sdept = 
'计算机'; 

-- 2 多表联合视图：选修1号课程的学生的视图

CREATE VIEW C1_STU(SNO, SNAME, SSEX, SAGE, GRADE) AS 
	SELECT
	    student.Sno,
	    student.Sname,
	    student.Ssex,
	    student.Sage,
	    sc.grade
	FROM student, sc
	WHERE
	    student.sno = sc.sno
	    AND sc.cno = 1
	WITH CHECK
OPTION; 

-- 添加了WITH CHECK OPTION后，如果对视图进行修改，则会对修改内容进行检查，检查规则遵循HWERE子句的内容

-- 3 查询视图：查询选修了1号课程的计算机系学生

SELECT
    CS_Stu.Sno,
    CS_Stu.Sname
FROM CS_Stu, sc
WHERE
    CS_Stu.Sno = sc.sno
    AND sc.cno = 1;

-- 4 更新视图：插入一个新的学生记录，学号201215129，姓名‘赵新’，年龄20

INSERT INTO CS_Stu SET Sno='201215129', Sname='赵新', Sage=20;

-- 设置了WITH CHECK OPTION，但是并不会像书上一样自动更新sdept的值，看了一篇[博客](https://blog.csdn.net/ClearLoveQ/article/details/84285060)后才知道MySQL是不支持这个操作的....所以只能插入基本表

INSERT INTO student
SET
    Sno = '201215129',
    Sname = '赵新',
    Ssex = '男',
    sdept = '计算机',
    Sage = 20;

-- 此时视图里面就有赵新了

-- 5 更新视图：更新值

UPDATE CS_Stu SET Sage=Sage - 1 WHERE Sname = '张三';

-- 二、在TPC_H数据库中实现

use TPC_H;

-- 1.建立关于供应商的视图

CREATE VIEW SUPPLIER_VIEW AS 
	SELECT
	    suppkey AS ID,
	    name,
	    address,
	    nationkey AS nation_ID,
	    phone
	FROM supplier
	WITH CHECK
OPTION; 

-- 2.建立在lineitem中出现的part信息的视图

CREATE VIEW LINEITEM_PART_VIEW AS 
	SELECT
	    partkey AS ID,
	    name,
	    mfgr,
	    type,
	    retailprice
	FROM part
	WHERE partkey IN (
	        SELECT
	            DISTINCT partkey
	        FROM lineitem
	    )
	WITH CHECK
OPTION; 

-- 3.建立part和supplier详细信息的视图

CREATE VIEW PART_SUPPLIER_VIEW AS 
	SELECT
	    part.partkey AS item_ID,
	    part.name AS item_name,
	    supplier.suppkey AS supplier_ID,
	    supplier.name AS supplier_name,
	    supplier.address AS supplier_address
	FROM
	    supplier,
	    part,
	    partsupp
	WHERE
	    supplier.suppkey = partsupp.suppkey
	    AND part.partkey = partsupp.p
PARTKEY; 

-- 4.建立关于各个region有多少个nation的视图

CREATE VIEW NATION_NUM_VIEW AS 
	SELECT
	    regionkey AS region_ID,
	    COUNT(nationkey) AS nation_num
	FROM nation
	GROUP BY(regionkey);
; 

-- 5. 更新视图

UPDATE lineitem_part_view
SET
    retailprice = retailprice * 0.9
WHERE ID < 1000;