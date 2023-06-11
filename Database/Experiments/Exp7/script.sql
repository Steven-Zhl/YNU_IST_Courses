# -- 定义各种完整性
# use student_course;

# -- 设置主键
# ALTER TABLE student
#     ADD PRIMARY KEY (sno);
# ALTER TABLE course
#     ADD PRIMARY KEY (cno);
# ALTER TABLE sc
#     ADD PRIMARY KEY (sno, cno);

# -- 定义用户定义完整性
# -- 逻辑上sc.sno参照student.sno，sc.cno参照course.cno，course.cpno参照course.cno，所以需要建立三组外键
# -- 在违约处理上，设置ON UPDATE CASCADE、ON DELETE NO ACTION当出现误输入或选课信息变动等情况时，只需要修改被参照表，sc中也会发生对应的变化；而当被参照表删除数据时，为尽量减小误删的损失，设置为删除时无操作
# ALTER TABLE sc
#     ADD FOREIGN KEY (sno) REFERENCES student (sno) ON UPDATE CASCADE;
# ALTER TABLE sc
#     ADD FOREIGN KEY (cno) REFERENCES course (cno) ON UPDATE CASCADE;
# ALTER TABLE course
#     ADD FOREIGN KEY (cpno) REFERENCES course (cno) ON UPDATE CASCADE;

# -- 设置用户定义完整性
# -- 课程号不能为null，且应该是唯一的
# ALTER TABLE course
#     MODIFY cno char(11) NOT NULL UNIQUE ;
# -- 学分不能为null
# ALTER TABLE course
#     MODIFY ccredit SMALLINT NOT NULL;
# -- 学号不能为null，且应该是唯一的
# ALTER TABLE student
#     MODIFY sno char(11) NOT NULL UNIQUE ;
# -- 年龄不能为null
# ALTER TABLE student
#     MODIFY sage smallint NOT NULL ;
# -- 所属的系部不能为null
# ALTER TABLE student
#     MODIFY sdept char(20) NOT NULL ;

# -- 测试完整性
use student_course;
# -- 测试实体完整性
# INSERT INTO student
# SET sno='201215129',
#     sname='temp',
#     sage=20,
#     sdept='计算机';

# -- 测试参照完整性
# INSERT INTO sc
# SET sno='test',
#     cno='1',
#     grade=0;

# -- 测试用户定义完整性
# INSERT INTO course
# SET cno='test',
#     cname='test-course',
#     cpno=null,
#     ccredit=null;


-- Ques2
# use tpc_h;
# -- 对于supplier，在修改后，检测其phone的格式是否正确，不正确则显示出来
# DELIMITER $$
# CREATE TRIGGER check_phone_format
#     BEFORE UPDATE
#     ON supplier
#     FOR EACH ROW
# BEGIN
#     IF CONVERT(NEW.phone, char) NOT REGEXP '^1\d{10}$' THEN
#         SET NEW.phone = null;
#     END IF;
# END$$
# DELIMITER ;
#
# drop trigger check_phone_format;