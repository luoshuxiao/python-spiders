#  与数据库mysql交互，连接数据库，插入数据，关闭连接

import pymysql


# 获取数据库连接
def get_connection():
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = '123456'
    database = 'qichamao'
    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)
    return db


# 获取数据库游标
def get_cursor(db):
    cursor = db.cursor()
    return cursor


# 关闭游标
def close_cursor(db):
    db.close()


# 企查猫网，插入数据库
def insert_data_mogujie(db, cursor, item):
    #  execute函数传参，间接插入数据 （函数对插入的参数进行处理，没有sql注入的风险）
    sql = "insert into company (company_name, c_name, c_phone, c_email) values (%s,%s,%s,%s)"
    print(sql)
    cursor.execute(sql, (item['CompanyName'], item['c_name'], item['c_phone'], item['c_email']))
    db.commit()