#-*- coding:utf-8 -*-
# author:cjx
# datetime:2020/3/19 22:53

# -*- coding: UTF-8 -*-
import mysql.connector

if __name__ == '__main__':
       # 打开数据库连接
       db = mysql.connector.connect(
              host="bigdata-pro01",
              user="root",
              passwd="123456", # 写上你的数据库密码
              database='chenyang',
              auth_plugin='mysql_native_password' # 密码验证方式，采用明文
       )
       # 获取操作游标
       cursor = db.cursor()
       # 执行SQL语句
       cursor.execute("SELECT VERSION()")
       # 获取一条数据
       data = cursor.fetchone()
       print("MySQL版本: %s " % data)
       # 关闭游标&数据库连接
       cursor.close()
       db.close()