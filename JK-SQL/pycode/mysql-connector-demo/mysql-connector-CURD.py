#-*- coding:utf-8 -*-
# author:cjx
# datetime:2020/3/21 15:30

import mysql.connector

if __name__ == '__main__':
    # 打开数据库连接
    db = mysql.connector.connect(
        host="bigdata-pro01",
        user="root",
        passwd="123456",  # 写上你的数据库密码
        database='chenyang',
        auth_plugin='mysql_native_password'  # 密码验证方式，采用明文
    )

    # 获取操作游标
    cursor = db.cursor()

    # 增加数据。
    # 在 player 表中增加一名新球员，姓名为“约翰·科林斯”，球队 ID 为 1003（即亚特兰大老鹰），身高为 2.08m。

    # 插入新球员
    # sql = "INSERT INTO player (team_id, player_name, height) VALUES (%s, %s, %s)"
    # val = (1003, "约翰-科林斯", 2.08)
    # cursor.execute(sql, val)
    # db.commit()
    # print(cursor.rowcount, "记录插入成功。")
    '''
    使用 cursor.execute 来执行相应的 SQL 语句，val 为 SQL 语句中的参数，SQL 执行后使用 db.commit() 进行提交。
    在使用 SQL 语句的时候，可以向 SQL 语句传递参数，这时 SQL 语句里要统一用（%s）进行占位，否则就会报错。
    不论插入的数值为整数类型，还是浮点类型，都需要统一用（%s）进行占位。
    
    在用游标进行 SQL 操作之后，还需要使用 db.commit() 进行提交，否则数据不会被插入。
    '''

    # 读取数据
    # 查询下身高大于等于 2.08m 的球员都有哪些

    # 查询身高大于等于2.08的球员
    # sql = 'SELECT player_id, player_name, height FROM player WHERE height>=2.08'
    # cursor.execute(sql)
    # data = cursor.fetchall()
    # for each_player in data:
    #     print(each_player)

    # 修改数据
    # 修改刚才插入的球员约翰·科林斯的身高，将身高修改成 2.09

    # 修改球员约翰-科林斯
    # sql = 'UPDATE player SET height = %s WHERE player_name = %s'
    # val = (2.09, "约翰-科林斯")
    # cursor.execute(sql, val)
    # db.commit()
    # print(cursor.rowcount, "记录被修改。")


    # 删除约翰·科林斯

    sql = 'DELETE FROM player WHERE player_name = %s'
    # 末尾要加一个 ，(逗号)。原因：加逗号才是元组
    val = ("约翰-科林斯",)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "记录删除成功。")

    # 关闭游标&数据库连接
    cursor.close()
    db.close()

    # 注意

    # 1. 打开数据库连接以后，如果不再使用，则需要关闭数据库连接，以免造成资源浪费。
    # 2. 在对数据进行增加、删除和修改的时候，可能会出现异常，这时就需要用try...except捕获异常信息。比如针对插入球员约翰·科林斯这个操作，你可以写成下面这样：
    import traceback

    try:
        sql = "INSERT INTO player (team_id, player_name, height) VALUES (%s, %s, %s)"
        val = (1003, "约翰-科林斯", 2.08)
        cursor.execute(sql, val)
        db.commit()
        print(cursor.rowcount, "记录插入成功。")
    except Exception as e:
        # 打印异常信息
        traceback.print_exc()
        # 回滚
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()
    # 3. 如果你在使用 mysql-connector 连接的时候，系统报的错误为authentication plugin caching_sha2，这时你需要下载最新的版本更新来解决，点击这里进行更新。