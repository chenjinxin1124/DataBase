# 数据准备
## 创建数据库
```
create database db default character set utf8mb4;
```
## 创建表
```
use db;
create table `t1` (
  `id` int(11) default null,
  `name` varchar(20) default null
) engine=innodb default charset=utf8mb4;
```
## 插入数据
```
insert into t1(id,name) select 101,'tome101';
insert into t1(id,name) select 102,'tome102';
insert into t1(id,name) select 103,'tome103';
insert into t1(id,name) select 104,'tome104';
insert into t1(id,name) select 105,'tome105';
insert into t1(id,name) select 106,'tome106';
insert into t1(id,name) select 107,'tome107';
insert into t1(id,name) select 108,'tome108';
```
## 更新数据
```
update t1 set name='jack101' where id=101;
update t1 set name='jack103' where id=103;
update t1 set name='jack105' where id=105;
```
## 删除数据
```
delete from t1 where id=102;
delete from t1 where id=104;
delete from t1 where id=106;
```
# 二进制日志
## 查看当前mysqlbinlog位置
https://dev.mysql.com/doc/refman/5.7/en/mysqlbinlog.html
```
➜  / which mysqlbinlog
/usr/bin/mysqlbinlog
```
## 查看binlog位置
```
mysql> show variables like '%log_bin%';
+---------------------------------+--------------------------------+
| Variable_name                   | Value                          |
+---------------------------------+--------------------------------+
| log_bin                         | ON                             |
| log_bin_basename                | /var/lib/mysql/mysql-bin       |
| log_bin_index                   | /var/lib/mysql/mysql-bin.index |
| log_bin_trust_function_creators | OFF                            |
| log_bin_use_v1_row_events       | OFF                            |
| sql_log_bin                     | ON                             |
+---------------------------------+--------------------------------+
6 rows in set (0.00 sec)
```
### 查看binlog 日志内容
/usr/bin/mysqlbinlog --no-defaults --database=db  --start-datetime='2021-04-07 00:00:00' --stop-datetime='2021-04-07 17:00:00'  mysql-bin.000001 | more
#### 可读
/usr/bin/mysqlbinlog --no-defaults --database=db  --base64-output=decode-rows -v   --start-datetime='2021-04-07 00:00:00' --stop-datetime='2021-04-07 17:00:00'  mysql-bin.000001 | more
#### 把binlog解析后的内容放到一个文件后，分析
/usr/bin/mysqlbinlog --no-defaults --database=db  --base64-output=decode-rows -v   --start-datetime='2021-04-07 00:00:00' --stop-datetime='2021-04-07 17:00:00'  mysql-bin.000001 | more >/tmp/binlog001.sql
# 全量备份
```
root@cjx:/var/lib/mysql# mysqldump -hlocalhost -uroot -p'password' -P3306 --single-transaction --master-data=2 db > db.sql
```
## 数据操作
```
mysql> flush logs;
Query OK, 0 rows affected (0.02 sec)

mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |      4323 |
| mysql-bin.000002 |       154 |
+------------------+-----------+
2 rows in set (0.00 sec)

mysql> select * from t1;
+------+---------+
| id   | name    |
+------+---------+
|  101 | jack101 |
|  103 | jack103 |
|  105 | jack105 |
|  107 | tome107 |
|  108 | tome108 |
+------+---------+
5 rows in set (0.00 sec)

mysql> delete from t1 where id>105;
Query OK, 2 rows affected (0.00 sec)

mysql> select * from t1;
+------+---------+
| id   | name    |
+------+---------+
|  101 | jack101 |
|  103 | jack103 |
|  105 | jack105 |
+------+---------+
3 rows in set (0.00 sec)

mysql> flush logs;
Query OK, 0 rows affected (0.02 sec)

mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |      4323 |
| mysql-bin.000002 |       474 |
| mysql-bin.000003 |       154 |
+------------------+-----------+
3 rows in set (0.00 sec)

mysql> show binlog events in 'mysql-bin.000002';
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                                   |
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
| mysql-bin.000002 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.31-0ubuntu0.18.04.1-log, Binlog ver: 4 |
| mysql-bin.000002 | 123 | Previous_gtids |         1 |         154 |                                                        |
| mysql-bin.000002 | 154 | Anonymous_Gtid |         1 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                   |
| mysql-bin.000002 | 219 | Query          |         1 |         289 | BEGIN                                                  |
| mysql-bin.000002 | 289 | Table_map      |         1 |         335 | table_id: 110 (db.t1)                                  |
| mysql-bin.000002 | 335 | Delete_rows    |         1 |         396 | table_id: 110 flags: STMT_END_F                        |
| mysql-bin.000002 | 396 | Xid            |         1 |         427 | COMMIT /* xid=912 */                                   |
| mysql-bin.000002 | 427 | Rotate         |         1 |         474 | mysql-bin.000003;pos=4                                 |
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
8 rows in set (0.00 sec)

mysql> insert into t1(id,name) select 109,'tome109';
Query OK, 1 row affected (0.01 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> insert into t1(id,name) select 110,'tome110';
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> select * from t1;
+------+---------+
| id   | name    |
+------+---------+
|  101 | jack101 |
|  103 | jack103 |
|  105 | jack105 |
|  109 | tome109 |
|  110 | tome110 |
+------+---------+
5 rows in set (0.00 sec)

mysql> flush logs;
Query OK, 0 rows affected (0.00 sec)

mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |      4323 |
| mysql-bin.000002 |       474 |
| mysql-bin.000003 |       721 |
| mysql-bin.000004 |       154 |
+------------------+-----------+
4 rows in set (0.00 sec)

mysql> drop table t1;
Query OK, 0 rows affected (0.01 sec)

mysql> show tables;
Empty set (0.00 sec)
```
# 恢复
## 全量恢复
```
bash-4.2# mysql -hlocalhost -uroot -p'password' -P3306 < /mysql_data/db.sql
或
source /mysql_data/db.sql

mysql> select * from t1;
+------+---------+
| id   | name    |
+------+---------+
|  101 | jack101 |
|  103 | jack103 |
|  105 | jack105 |
|  107 | tome107 |
|  108 | tome108 |
+------+---------+
5 rows in set (0.00 sec)
```
## 增量恢复
恢复mysql-bin.000001
```
root@cjx:/var/lib/mysql# mysqlbinlog mysql-bin.000001 |mysql  -hlocalhost -uroot -p'password' -P3306
```
### 部分恢复
```
在general_log中找到误删除的时间点，然后更加对应的时间点到bin-log.000003中找到相应的position点，需要恢复到误删除的前面一个position点。
可以用如下参数来控制binlog的区间
--start-position 开始点 --stop-position 结束点
--start-date 开始时间  --stop-date  结束时间
```
```
mysql> show binlog events in 'mysql-bin.000002';
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                                   |
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
| mysql-bin.000002 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.31-0ubuntu0.18.04.1-log, Binlog ver: 4 |
| mysql-bin.000002 | 123 | Previous_gtids |         1 |         154 |                                                        |
| mysql-bin.000002 | 154 | Anonymous_Gtid |         1 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                   |
| mysql-bin.000002 | 219 | Query          |         1 |         289 | BEGIN                                                  |
| mysql-bin.000002 | 289 | Table_map      |         1 |         335 | table_id: 110 (db.t1)                                  |
| mysql-bin.000002 | 335 | Delete_rows    |         1 |         396 | table_id: 110 flags: STMT_END_F                        |
| mysql-bin.000002 | 396 | Xid            |         1 |         427 | COMMIT /* xid=912 */                                   |
| mysql-bin.000002 | 427 | Rotate         |         1 |         474 | mysql-bin.000003;pos=4                                 |
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
8 rows in set (0.00 sec)

mysql> show binlog events in 'mysql-bin.000003';
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                                   |
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
| mysql-bin.000003 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.31-0ubuntu0.18.04.1-log, Binlog ver: 4 |
| mysql-bin.000003 | 123 | Previous_gtids |         1 |         154 |                                                        |
| mysql-bin.000003 | 154 | Anonymous_Gtid |         1 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                   |
| mysql-bin.000003 | 219 | Query          |         1 |         289 | BEGIN                                                  |
| mysql-bin.000003 | 289 | Table_map      |         1 |         335 | table_id: 110 (db.t1)                                  |
| mysql-bin.000003 | 335 | Write_rows     |         1 |         383 | table_id: 110 flags: STMT_END_F                        |
| mysql-bin.000003 | 383 | Xid            |         1 |         414 | COMMIT /* xid=973 */                                   |
| mysql-bin.000003 | 414 | Anonymous_Gtid |         1 |         479 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                   |
| mysql-bin.000003 | 479 | Query          |         1 |         549 | BEGIN                                                  |
| mysql-bin.000003 | 549 | Table_map      |         1 |         595 | table_id: 110 (db.t1)                                  |
| mysql-bin.000003 | 595 | Write_rows     |         1 |         643 | table_id: 110 flags: STMT_END_F                        |
| mysql-bin.000003 | 643 | Xid            |         1 |         674 | COMMIT /* xid=974 */                                   |
| mysql-bin.000003 | 674 | Rotate         |         1 |         721 | mysql-bin.000004;pos=4                                 |
+------------------+-----+----------------+-----------+-------------+--------------------------------------------------------+
13 rows in set (0.00 sec)

 mysqlbinlog mysql-bin.000003  --start-position=219 --stop-position=414 |mysql  -hlocalhost -uroot -p'password' -P3306

 mysql> select * from t1;
+------+---------+
| id   | name    |
+------+---------+
|  101 | jack101 |
|  103 | jack103 |
|  105 | jack105 |
|  107 | tome107 |
|  108 | tome108 |
|  109 | tome109 |
+------+---------+
6 rows in set (0.00 sec)

```