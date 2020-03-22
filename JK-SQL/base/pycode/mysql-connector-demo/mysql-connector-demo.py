#-*- coding:utf-8 -*-
# author:cjx
# datetime:2020/3/19 22:53

# -*- coding: UTF-8 -*-
import mysql.connector

if __name__ == '__main__':
       # Connection 就是对数据库的当前连接进行管理
       '''
       1. 通过指定 host、user、passwd 和 port 等参数来创建数据库连接，这些参数分别对应着数据库 IP 地址、用户名、密码和端口号；
       2. 使用 db.close() 关闭数据库连接；
       3. 使用 db.cursor() 创建游标，操作数据库中的数据；
       4. 使用 db.begin() 开启事务；
       5. 使用 db.commit() 和 db.rollback()，对事务进行提交以及回滚。
       '''
       # 打开数据库连接
       db = mysql.connector.connect(
              host="bigdata-pro01",
              user="root",
              passwd="123456", # 写上你的数据库密码
              database='chenyang',
              auth_plugin='mysql_native_password' # 密码验证方式，采用明文
       )
       #当我们通过cursor = db.cursor()创建游标后，就可以通过面向过程的编程方式对数据库中的数据进行操作：
       '''
       1. 使用cursor.execute(query_sql)，执行数据库查询；
       2. 使用cursor.fetchone()，读取数据集中的一条数据；
       3. 使用cursor.fetchall()，取出数据集中的所有行，返回一个元组 tuples 类型；
       4. 使用cursor.fetchmany(n)，取出数据集中的多条数据，同样返回一个元组 tuples；
       5. 使用cursor.rowcount，返回查询结果集中的行数。如果没有查询到数据或者还没有查询，则结果为 -1，否则会返回查询得到的数据行数；
       6. 使用cursor.close()，关闭游标。
       '''
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