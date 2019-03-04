-- sql语句

create database mogujie default character set='utf8';
use mogujie;
create table goods(
   id int primary key auto_increment,
   trade_id varchar(256),
   img varchar(1024),
   title varchar(256),
   link varchar(1024),
   org_price varchar(32),
   price varchar(32)
);
