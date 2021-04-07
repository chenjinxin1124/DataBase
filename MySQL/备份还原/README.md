# 启用了二进制日志记录
https://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html
```
find / -name my.cnf
vim /etc/my.cnf

添加
[mysqld]
log-bin=mysql-bin
server-id=1
```
重启服务
# 查看log_bin
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
```
## 查看binlog相关参数
```
mysql> show variables like "%binlog%";
+--------------------------------------------+----------------------+
| Variable_name                              | Value                |
+--------------------------------------------+----------------------+
| binlog_cache_size                          | 32768                |
| binlog_checksum                            | CRC32                |
| binlog_direct_non_transactional_updates    | OFF                  |
| binlog_error_action                        | ABORT_SERVER         |
| binlog_format                              | ROW                  |
| binlog_group_commit_sync_delay             | 0                    |
| binlog_group_commit_sync_no_delay_count    | 0                    |
| binlog_gtid_simple_recovery                | ON                   |
| binlog_max_flush_queue_time                | 0                    |
| binlog_order_commits                       | ON                   |
| binlog_row_image                           | FULL                 |
| binlog_rows_query_log_events               | OFF                  |
| binlog_stmt_cache_size                     | 32768                |
| binlog_transaction_dependency_history_size | 25000                |
| binlog_transaction_dependency_tracking     | COMMIT_ORDER         |
| innodb_api_enable_binlog                   | OFF                  |
| innodb_locks_unsafe_for_binlog             | OFF                  |
| log_statements_unsafe_for_binlog           | ON                   |
| max_binlog_cache_size                      | 18446744073709547520 |
| max_binlog_size                            | 1073741824           |
| max_binlog_stmt_cache_size                 | 18446744073709547520 |
| sync_binlog                                | 1                    |
+--------------------------------------------+----------------------+
22 rows in set (0.00 sec)
```
## 查看目录
```
bash-4.2# pwd
/var/lib/mysql
bash-4.2# ls
auto.cnf    ca.pem	     client-key.pem  ib_logfile0  ibdata1  mysql	     mysql-bin.index  mysql.sock.lock	  private_key.pem  server-cert.pem  sys   wise_bot_management_platform
ca-key.pem  client-cert.pem  ib_buffer_pool  ib_logfile1  ibtmp1   mysql-bin.000001  mysql.sock       performance_schema  public_key.pem   server-key.pem   test
```
## 查看当前正在写入的binlog文件
```
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      313 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.01 sec)
```
## 查看当前正在写入的日志文件中的binlog事件
```
mysql> show binlog events;
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                  |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| mysql-bin.000001 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.31-log, Binlog ver: 4 |
| mysql-bin.000001 | 123 | Previous_gtids |         1 |         154 |                                       |
| mysql-bin.000001 | 154 | Anonymous_Gtid |         1 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| mysql-bin.000001 | 219 | Query          |         1 |         313 | create database test                  |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
4 rows in set (0.01 sec)
```
## 查看指定的文件
```
mysql> show binlog events in 'mysql-bin.000001';
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                  |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| mysql-bin.000001 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.31-log, Binlog ver: 4 |
| mysql-bin.000001 | 123 | Previous_gtids |         1 |         154 |                                       |
| mysql-bin.000001 | 154 | Anonymous_Gtid |         1 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| mysql-bin.000001 | 219 | Query          |         1 |         313 | create database test                  |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
4 rows in set (0.00 sec)
```
## 显示文件列表
```
mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |       313 |
+------------------+-----------+
1 row in set (0.00 sec)
```

# 全量备份
```
备份命令mysqldump格式
格式：mysqldump -h主机名  -P端口 -u用户名 -p密码 –database 数据库名 > 文件名.sql 

备份MySQL数据库为带删除表的格式，能够让该备份覆盖已有数据库而不需要手动删除原有数据库。
mysqldump  --add-drop-table -uusername -ppassword -database databasename > backupfile.sql

直接将MySQL数据库压缩备份
mysqldump -hhostname -uusername -ppassword -database databasename | gzip > backupfile.sql.gz

备份MySQL数据库某个(些)表
mysqldump -hhostname -uusername -ppassword databasename specific_table1 specific_table2 > backupfile.sql

同时备份多个MySQL数据库
mysqldump -hhostname -uusername -ppassword –databases databasename1 databasename2 databasename3 > multibackupfile.sql

仅备份份数据库结构
mysqldump –no-data –databases databasename1 databasename2 databasename3 > structurebackupfile.sql

备份服务器上所有数据库
mysqldump –all-databases > allbackupfile.sql

还原MySQL数据库的命令
mysql -hhostname -uusername -ppassword databasename < backupfile.sql

还原压缩的MySQL数据库
gunzip < backupfile.sql.gz | mysql -uusername -ppassword databasename

将数据库转移到新服务器
mysqldump -uusername -ppassword databasename | mysql –host=*.*.*.* -C databasename
```