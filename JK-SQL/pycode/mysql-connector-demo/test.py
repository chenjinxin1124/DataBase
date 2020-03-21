# -*- coding:utf-8 -*-
# author:cjx
# datetime:2020/3/21 15:43

'''
对 heros 表中最大生命值大于 6000 的英雄进行查询，并且输出相应的属性值。
'''

import mysql.connector
import traceback
import json

if __name__ == '__main__':
    # 读取数据库链接配置文件
    with open('mysql.json', encoding='utf-8') as con_json:
        con_dict = json.load(con_json)

    # 打开数据库连接
    db = mysql.connector.connect(
        host=con_dict['host'],
        user=con_dict['user'],
        passwd=con_dict['passwd'],
        database=con_dict['database'],
        auth_plugin=con_dict['auth_plugin'],
    )

    # 获取操作游标
    cursor = db.cursor()

    try:
        sql = 'SELECT  id, name, hp_max FROM heros where hp_max > %s'
        # 注意：val里面的元素后面必须要加英文逗号，不加或者中文逗号都会报错(末尾要加一个 ，(逗号)。原因：加逗号才是元组)
        val = (6000,)
        cursor.execute(sql, val)
        data = cursor.fetchall()
        print(cursor.rowcount, '查询成功。')
        for each_player in data:
            print(each_player)
    except Exception as e:
        # 打印异常信息
        traceback.print_exc()
        # 回滚
        db.rollback()
    finally:
        # 关闭游标&数据库连接
        cursor.close()
        db.close()
