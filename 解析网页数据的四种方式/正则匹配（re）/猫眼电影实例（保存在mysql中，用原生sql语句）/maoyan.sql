-- sql语句

create database maoyan default character set='utf8';
use maoyan;
create table movie(
   id int primary key  auto_increment,
   title varchar(256),
   actor varchar(256),
   detail varchar(1024),
   img_url varchar(1024)
);