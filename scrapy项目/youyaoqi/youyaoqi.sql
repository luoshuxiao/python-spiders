-- sql语句

create database youyaoqi default character set='utf8';
use youyaoqi;
create table comic(
   id int primary key auto_increment,
   comic_id varchar(32),
   name varchar(32),
   cover varchar(1024),
   line2 varchar(32)
);