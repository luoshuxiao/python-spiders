#  与数据库mysql交互，连接数据库，插入数据，关闭连接

import pymysql


# 获取数据库连接
def get_connection():
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = '123456'
    database = 'mogujie'
    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)
    return db


# 获取数据库游标
def get_cursor(db):
    cursor = db.cursor()
    return cursor


# 关闭游标
def close_cursor(db):
    db.close()


# 猫眼网，插入数据库
def insert_data(db, cursor, item):
    #  方法一：字符串占位匹配sql语句，直接插入数据 （有sql注入的风险）
    sql = "insert into movie (title, actor, detail, img_url) values ('%s','%s','%s','%s');" % (item['move_name'], item['actor'], item['detail'], item['img'])
    print(sql)
    cursor.execute(sql)
    db.commit()


# 蘑菇街网，插入数据库
def insert_data_mogujie(db, cursor, item):
    #  方法二：execute函数传参，间接插入数据 （函数对插入的参数进行处理，没有sql注入的风险）
    sql = "insert into goods (trade_id, img, title, link, org_price, price) values (%s,%s,%s,%s,%s,%s)"
    print(sql)
    cursor.execute(sql, (item['tradeItemId'], item['img'], item['title'], item['link'], item['orgPrice'], item['price']))
    db.commit()