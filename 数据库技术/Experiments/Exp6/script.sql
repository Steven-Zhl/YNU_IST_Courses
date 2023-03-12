-- Active: 1663424224542@@127.0.0.1@3306

-- 创建账户abc

CREATE USER 'abc'@'localhost' IDENTIFIED BY 'password_abc';

-- 创建账户def

CREATE USER 'def'@'localhost';

SET PASSWORD FOR 'def'@'localhost'='password_def';

-- 将abc设为管理员

GRANT ALL PRIVILEGES ON *.* TO 'abc'@'localhost' WITH GRANT OPTION;