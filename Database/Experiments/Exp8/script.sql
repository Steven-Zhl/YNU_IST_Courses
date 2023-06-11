-- 1.

-- 创建存储过程：输入课程名，计算并输出该课程的平均分
CREATE PROCEDURE `course_ave_procedure`(cname char(10))
BEGIN
    declare grade_avg float; -- 课程平均分
    declare cur_grade_avg cursor for
        select cname, avg(sc.grade)
        from sc
        where sc.cno = (select cno from course where course.cname = cname);
    -- 游标
    create table if not exists tbl_avg_grade
    (
        cname char(10),
        ave   float
    );-- 创建暂存结果的表
    open cur_grade_avg;
    fetch cur_grade_avg into cname, grade_avg;
    close cur_grade_avg;
    if exists(select * from tbl_avg_grade where tbl_avg_grade.cname = cname) then
        update tbl_avg_grade
        set ave = grade_avg
        where cname = cname;
    else
        insert into tbl_avg_grade()
        values (cname, grade_avg);
    end if; -- 将结果插入到表中
END;
-- 调用存储过程
CALL course_ave_procedure('C语言');

-- 2.

-- 创建函数实现：输入课程名，计算并返回该课程的平均分
set global log_bin_trust_function_creators = TRUE;
CREATE FUNCTION `course_ave_function`(cname char(10)) RETURNS float
BEGIN
    declare grade_avg float;
    select avg(sc.grade)
    into grade_avg
    from sc
    where sc.cno = (select cno from course where course.cname = cname);
    return grade_avg;
END;
-- 调用函数
SELECT course_ave_function('C语言');

-- 3.

-- 创建存储过程：计算每门课程的平均分，将平均分低于70分的课程号、课程名、平均分存入表中
CREATE PROCEDURE `course_ave_procedure2`()
BEGIN
    declare cno char(11);
    declare cname char(10);
    declare grade_avg float;
    declare flag int;
    declare cur_course_avg cursor for
        select course.cno, course.cname, avg(sc.grade)
        from course,
             sc
        where course.cno = sc.cno
        group by course.cno;
    -- 游标
    DECLARE CONTINUE HANDLER FOR NOT
        FOUND SET flag = 1;
    set flag = 0;
    drop table if exists fail_course;
    create table fail_course
    (
        cno      char(11),
        cname    char(10),
        avegrade float
    );-- 创建暂存结果的表
    open cur_course_avg;
    fetch cur_course_avg into cno, cname, grade_avg;
    while (not flag)
        do
            if (grade_avg < 70) then
                insert into fail_course values (cno, cname, grade_avg);
            end if;
            fetch cur_course_avg into cno, cname, grade_avg;
        end while;
    close cur_course_avg;
END;
-- 调用存储过程
CALL course_ave_procedure2();

-- 4.

-- 创建存储过程：统计各个region中的customer人数
CREATE PROCEDURE `customer_count_by_region_procedure`()
BEGIN
    declare region_name text;
    declare customer_count int;
    declare flag int;
    declare cur_customer_count cursor for
        select region.name, count(customer.custkey)
        from region,
             nation,
             customer
        where region.regionkey = nation.regionkey
          and nation.nationkey = customer.nationkey
        group by region.name;
    -- 游标
    DECLARE CONTINUE HANDLER FOR NOT
        FOUND SET flag = 1;
    set flag = 0;
    drop table if exists tbl_customer_count_by_region;
    create table tbl_customer_count_by_region
    (
        region_name    text,
        customer_count int
    );-- 创建暂存结果的表
    open cur_customer_count;
    fetch cur_customer_count into region_name, customer_count;
    while (not flag)
        do
            insert into tbl_customer_count_by_region values (region_name, customer_count);
            fetch cur_customer_count into region_name, customer_count;
        end while;
    close cur_customer_count;
END;
-- 调用存储过程
CALL customer_count_by_region_procedure();

-- 5.

-- 创建函数：返回某个region中的supplier个数
CREATE FUNCTION `supplier_count_by_region_function`(region_name text) RETURNS int
BEGIN
    declare supplier_count int;
    select count(supplier.suppkey)
    into supplier_count
    from supplier,
         nation,
         region
    where supplier.nationkey = nation.nationkey
      and nation.regionkey = region.regionkey
      and region.name = region_name;

    return supplier_count;
END;
-- 调用函数过程
SELECT supplier_count_by_region_function('亚洲');