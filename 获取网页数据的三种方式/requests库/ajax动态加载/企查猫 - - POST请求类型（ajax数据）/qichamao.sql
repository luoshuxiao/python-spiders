-- sql语句

create database qichamao default character set='utf8';
use qichamao;
create table company(
   id int primary key auto_increment,
   company_name varchar(64),
   c_name varchar(32),
   c_phone varchar(16),
   c_email varchar(64)
);