检查log-bin是否开启
```
mysql> show variables like 'log_bin';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| log_bin       | OFF   |
+---------------+-------+
1 row in set (0.00 sec)
```

开始配置log-bin，并启动log-bin<br>
查找mysql的配置文件：
```
[kfk@bigdata-pro01 ~]$ sudo find / -name my.cnf
/etc/my.cnf
```
修改配置文件
添加一行：log-bin=mysql-bin
```
[kfk@bigdata-pro01 ~]$ sudo vim /etc/my.cnf
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
user=mysql
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
default-character-set=utf8
log-bin=mysql-bin #####################################

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
default-character-set=utf8

[client]
default-character-set=utf8
```
重启mysql：
```
[kfk@bigdata-pro01 ~]$ sudo service mysqld restart
Stopping mysqld:                                           [  OK  ]
Starting mysqld:                                           [  OK  ]
```
登录：[kfk@bigdata-pro01 ~]$ mysql -uroot -p<br>
检查log-bin是否开启：
```
mysql> show variables like 'log_bin';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| log_bin       | ON    |
+---------------+-------+
1 row in set (0.00 sec)
```
查看目前的binlog文件
```
mysql> show master logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |       189 |
+------------------+-----------+
1 row in set (0.00 sec)
```
查看日志文件位置：
```
[kfk@bigdata-pro01 ~]$ sudo find / -name mysql-bin.000001
/var/lib/mysql/mysql-bin.000001
```
进入该位置，并使用mysqlbinlog查看日志文件：
```
[kfk@bigdata-pro01 ~]$ cd /var/lib/mysql
[kfk@bigdata-pro01 mysql]$ mysqlbinlog --no-defaults  mysql-bin.000001
/*!40019 SET @@session.max_insert_delayed_threads=0*/;
/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
DELIMITER /*!*/;
mysqlbinlog: File 'mysql-bin.000001' not found (Errcode: 13)
DELIMITER ;
# End of log file
ROLLBACK /* added by mysqlbinlog */;
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
```
查看日志文件内容
```
[kfk@bigdata-pro01 mysql]$ sudo mysqlbinlog /var/lib/mysql/mysql-bin.000001      
mysqlbinlog: unknown variable 'default-character-set=utf8'
[kfk@bigdata-pro01 mysql]$ sudo mysqlbinlog --no-defaults /var/lib/mysql/mysql-bin.000001
/*!40019 SET @@session.max_insert_delayed_threads=0*/;
/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
DELIMITER /*!*/;
# at 4
#200304 14:31:35 server id 1  end_log_pos 106   Start: binlog v 4, server v 5.1.73-log created 200304 14:31:35 at startup
# Warning: this binlog is either in use or was not closed properly.
ROLLBACK/*!*/;
BINLOG '
R0tfXg8BAAAAZgAAAGoAAAABAAQANS4xLjczLWxvZwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAABHS19eEzgNAAgAEgAEBAQEEgAAUwAEGggAAAAICAgC
'/*!*/;
# at 106
#200304 14:33:20 server id 1  end_log_pos 189   Query   thread_id=2     exec_time=0     error_code=0
use `chenyang`/*!*/;
SET TIMESTAMP=1583303600/*!*/;
SET @@session.pseudo_thread_id=2/*!*/;
SET @@session.foreign_key_checks=1, @@session.sql_auto_is_null=1, @@session.unique_checks=1, @@session.autocommit=1/*!*/;
SET @@session.sql_mode=0/*!*/;
SET @@session.auto_increment_increment=1, @@session.auto_increment_offset=1/*!*/;
/*!\C utf8 *//*!*/;
SET @@session.character_set_client=33,@@session.collation_connection=33,@@session.collation_server=33/*!*/;
SET @@session.lc_time_names=0/*!*/;
SET @@session.collation_database=DEFAULT/*!*/;
drop table heros
/*!*/;
DELIMITER ;
# End of log file
ROLLBACK /* added by mysqlbinlog */;
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
```
**恢复**<br>
1. 准备
```
mysql> CREATE TABLE test(id INT);
Query OK, 0 rows affected (0.01 sec)
mysql> INSERT INTO test VALUES(1),(2),(3);  
Query OK, 3 rows affected (0.00 sec)
mysql> SELECT * FROM test;
+------+
| id   |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```
2. 首先，看下当前binlog位置
```
mysql> show master status;
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000001 |    27528 |              |                  |
+------------------+----------+--------------+------------------+
1 row in set (0.00 sec)

```
3. 向表tb_person中插入两条记录：
```
mysql> INSERT INTO test VALUES(4),(5);
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
``` 
4. 记录当前binlog位置：
```
mysql> show master status;
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000001 |    27625 |              |                  |
+------------------+----------+--------------+------------------+
1 row in set (0.00 sec)
```
5. 查询数据 
```
mysql> SELECT * FROM test;
+------+
| id   |
+------+
|    1 |
|    2 |
|    3 |
|    4 |
|    5 |
+------+
5 rows in set (0.00 sec)
```
6. 删除3条: 
```
mysql> delete from test where id > 1 AND id < 5;
Query OK, 3 rows affected (0.00 sec)
```
7. binlog恢复（指定pos点恢复/部分恢复）
```
[root@bigdata-pro01 mysql]# mysqlbinlog --no-defaults --start-position=27528 --stop-position=27625 /var/lib/mysql/mysql-bin.000001 > test.sql

mysql> source /var/lib/mysql/test.sql
```
8. 数据恢复完成 

9. 总结





#### 使用开源工具 binlog2sql
**虚拟机要自动获取地址，连接外网才能安装**
安装开源工具binlog2sql。binlog2sql是一款简单易用的binlog解析工具，其中一个功能就是生成回滚SQL。
```
安装git
[kfk@bigdata-pro01 ~]$ sudo yum install -y git
git clone https://github.com/danfengcao/binlog2sql.git
```

