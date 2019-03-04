create database jd default character set='utf8';
use jd;

create table goods(
    id int primary key auto_increment,
    title varchar(128),
    img varchar(1024),
    price varchar(32),
    sku varchar(32),
    detail varchar(1024)
);