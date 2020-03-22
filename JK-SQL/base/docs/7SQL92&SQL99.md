在数据库中，表的组成是基于关系模型的，所以一个表就是一个关系。一个数据库中可以包括多个表，也就是存在多种数据之间的关系。而我们之所以能使用 SQL 语言对各个数据表进行复杂查询，核心就在于连接，它可以用一条 SELECT 语句在多张表之间进行查询。你也可以理解为，关系型数据库的核心之一就是连接。

### 在 SQL92 中是如何使用连接的
SQL92 中的 5 种连接方式，它们分别是笛卡尔积、等值连接、非等值连接、外连接（左连接、右连接）和自连接。

#### 笛卡尔积
笛卡尔乘积是一个数学运算。假设我有两个集合 X 和 Y，那么 X 和 Y 的笛卡尔积就是 X 和 Y 的所有可能组合，也就是第一个对象来自于 X，第二个对象来自于 Y 的所有可能。
```
mysql> SELECT * FROM player;
37 rows in set (0.00 sec)

mysql> SELECT * FROM team;
3 rows in set (0.00 sec)

mysql> SELECT * FROM player, team;
111 rows in set (0.00 sec)
```
笛卡尔积也称为交叉连接，英文是 CROSS JOIN，它的作用就是可以把任意表进行连接，即使这两张表不相关。但我们通常进行连接还是需要筛选的，因此你需要在连接后面加上 WHERE 子句，也就是作为过滤条件对连接数据进行筛选。比如后面要讲到的等值连接。

#### 等值连接
两张表的等值连接就是用两张表中都存在的列进行连接。我们也可以对多张表进行等值连接。

针对 player 表和 team 表都存在 team_id 这一列，我们可以用等值连接进行查询。
```
mysql> SELECT player_id, player.team_id, player_name, height, team_name FROM player, team WHERE player.team_id = team.team_id;
37 rows in set (0.00 sec)
```

在进行等值连接的时候，可以使用表的别名，这样会让 SQL 语句更简洁：
```
mysql> SELECT player_id, a.team_id, player_name, height, team_name FROM player AS a, team AS b WHERE a.team_id = b.team_id;
```

需要注意的是，如果我们使用了表的别名，在查询字段中就只能使用别名进行代替，不能使用原有的表名，比如下面的 SQL 查询就会报错：
```
mysql> SELECT player_id, player.team_id, player_name, height, team_name FROM player AS a, team AS b WHERE a.team_id = b.team_id;
ERROR 1054 (42S22): Unknown column 'player.team_id' in 'field list'
```

#### 非等值连接
当我们进行多表查询的时候，如果连接多个表的条件是等号时，就是等值连接，其他的运算符连接就是非等值查询。

player 表中有身高 height 字段，如果想要知道每个球员的身高的级别，可以采用非等值连接查询。
```
mysql> SELECT p.player_name, p.height, h.height_level FROM player AS p, height_grades AS h WHERE p.height BETWEEN h.height_lowest AND h.height_highest;
37 rows in set (0.00 sec)
```

#### 外连接
除了查询满足条件的记录以外，外连接还可以查询某一方不满足条件的记录。两张表的外连接，会有一张是主表，另一张是从表。如果是多张表的外连接，那么第一张表是主表，即显示全部的行，而第剩下的表则显示对应连接的信息。在 SQL92 中采用（+）代表从表所在的位置，而且在 SQL92 中，只有左外连接和右外连接，没有全外连接。

左外连接，就是指左边的表是主表，需要显示左边表的全部行，而右侧的表是从表，（+）表示哪个是从表。
```
SQL92
mysql> SELECT * FROM player, team where player.team_id = team.team_id(+);
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ')' at line 1

SQL99:
mysql> SELECT * FROM player LEFT JOIN team on player.team_id = team.team_id;
37 rows in set (0.00 sec)
```

右外连接，指的就是右边的表是主表，需要显示右边表的全部行，而左侧的表是从表。
```
SQL：SELECT * FROM player, team where player.team_id(+) = team.team_id

mysql> SELECT * FROM player RIGHT JOIN team on player.team_id = team.team_id;
38 rows in set (0.00 sec)
```
LEFT JOIN 和 RIGHT JOIN 只存在于 SQL99 及以后的标准中，在 SQL92 中不存在，只能用（+）表示。

#### 自连接
查看比布雷克·格里芬高的球员都有谁，以及他们的对应身高：
```
mysql> SELECT b.player_name, b.height FROM player as a , player as b WHERE a.player_name = '布雷克-格里芬' and a.height < b.height;
+---------------------------+--------+
| player_name               | height |
+---------------------------+--------+
| 安德烈-德拉蒙德           |   2.11 |
| 索恩-马克                 |   2.16 |
| 扎扎-帕楚里亚             |   2.11 |
| 亨利-埃伦森               |   2.11 |
| 多曼塔斯-萨博尼斯         |   2.11 |
| 迈尔斯-特纳               |   2.11 |
+---------------------------+--------+
6 rows in set (0.00 sec)
```

Oracle 对 SQL92 支持较好，而 MySQL 则不支持 SQL92 的外连接。

#### test
这 3 支球队需要进行比赛，请用一条 SQL 语句显示出所有可能的比赛组合。
```
select CONCAT(kedui.team_name, ' VS ', zhudui.team_name) as '客队 VS 主队'
from team kedui, team zhudui
where kedui.team_id != zhudui.team_id;

mysql> select a.team_name, b.team_name
    -> from team a, team b
    -> where a.team_id != b.team_id;
+-----------------------+-----------------------+
| team_name             | team_name             |
+-----------------------+-----------------------+
| 印第安纳步行者        | 底特律活塞            |
| 亚特兰大老鹰          | 底特律活塞            |
| 底特律活塞            | 印第安纳步行者        |
| 亚特兰大老鹰          | 印第安纳步行者        |
| 底特律活塞            | 亚特兰大老鹰          |
| 印第安纳步行者        | 亚特兰大老鹰          |
+-----------------------+-----------------------+
6 rows in set (0.01 sec)

mysql> select CONCAT(kedui.team_name, ' VS ', zhudui.team_name) as '客队 VS 主队'
    -> from team kedui, team zhudui
    -> where kedui.team_id != zhudui.team_id;
+---------------------------------------------+
| 客队 VS 主队                                |
+---------------------------------------------+
| 印第安纳步行者 VS 底特律活塞                |
| 亚特兰大老鹰 VS 底特律活塞                  |
| 底特律活塞 VS 印第安纳步行者                |
| 亚特兰大老鹰 VS 印第安纳步行者              |
| 底特律活塞 VS 亚特兰大老鹰                  |
| 印第安纳步行者 VS 亚特兰大老鹰              |
+---------------------------------------------+
6 rows in set (0.00 sec)

select a.team_name, b.team_name
from team a, team b
where a.team_id < b.team_id;

mysql> select a.team_name, b.team_name
    -> from team a, team b
    -> where a.team_id < b.team_id;
+-----------------------+-----------------------+
| team_name             | team_name             |
+-----------------------+-----------------------+
| 底特律活塞            | 印第安纳步行者        |
| 底特律活塞            | 亚特兰大老鹰          |
| 印第安纳步行者        | 亚特兰大老鹰          |
+-----------------------+-----------------------+
3 rows in set (0.00 sec)
```

**查询顺序是**：FROM > WHERE > GROUP BY > HAVING > SELECT > DISTINCT > ORDER BY > LIMIT
