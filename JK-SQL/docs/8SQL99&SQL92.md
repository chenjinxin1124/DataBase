### SQL99 标准中的连接查询
#### 交叉连接
交叉连接实际上就是 SQL92 中的笛卡尔乘积，只是这里我们采用的是 CROSS JOIN。
```
mysql> SELECT * FROM player CROSS JOIN team;
111 rows in set (0.00 sec)
```
如果多张表进行交叉连接，比如表 t1，表 t2，表 t3 进行交叉连接，可以写成下面这样：
```
SELECT * FROM t1 CROSS JOIN t2 CROSS JOIN t3;
```

#### 自然连接
可以把自然连接理解为 SQL92 中的等值连接。它会帮你自动查询两张连接表中所有相同的字段，然后进行等值连接。

把 player 表和 team 表进行等值连接，相同的字段是 team_id。<br>
SQL92:
SELECT player_id, a.team_id, player_name, height, team_name FROM player as a, team as b WHERE a.team_id = b.team_id
SQL99:
SELECT player_id, team_id, player_name, height, team_name FROM player NATURAL JOIN team 

实际上，在 SQL99 中用 NATURAL JOIN 替代了 WHERE player.team_id = team.team_id。

#### ON 连接

ON 连接用来指定我们想要的连接条件，针对上面的例子，它同样可以帮助我们实现自然连接的功能：
```
mysql> SELECT player_id, player.team_id, player_name, height, team_name FROM player JOIN team ON player.team_id = team.team_id;
37 rows in set (0.00 sec)
```
也可以 ON 连接进行非等值连接，比如我们想要查询球员的身高等级，需要用 player 和 height_grades 两张表：
```
mysql> SELECT p.player_name, p.height, h.height_level FROM player as p JOIN height_grades as h ON height BETWEEN h.height_lowest AND h.height_highest;
+------------------------------------+--------+--------------+
| player_name                        | height | height_level |
+------------------------------------+--------+--------------+
| 韦恩-艾灵顿                        |   1.93 | B            |
| 雷吉-杰克逊                        |   1.91 | B            |
| 安德烈-德拉蒙德                    |   2.11 | A            |
| 索恩-马克                          |   2.16 | A            |
| 布鲁斯-布朗                        |   1.96 | B            |
| 兰斯顿-加洛韦                      |   1.88 | C            |
| 格伦-罗宾逊三世                    |   1.98 | B            |
| 伊斯梅尔-史密斯                    |   1.83 | C            |
| 扎扎-帕楚里亚                      |   2.11 | A            |
| 乔恩-洛伊尔                        |   2.08 | A            |
| 布雷克-格里芬                      |   2.08 | A            |
| 雷吉-巴洛克                        |   2.01 | A            |
| 卢克-肯纳德                        |   1.96 | B            |
| 斯坦利-约翰逊                      |   2.01 | A            |
| 亨利-埃伦森                        |   2.11 | A            |
| 凯里-托马斯                        |   1.91 | B            |
| 何塞-卡尔德隆                      |   1.91 | B            |
| 斯维亚托斯拉夫-米凯卢克            |   2.03 | A            |
| 扎克-洛夫顿                        |   1.93 | B            |
| 卡林-卢卡斯                        |   1.85 | C            |
| 维克多-奥拉迪波                    |   1.93 | B            |
| 博扬-博格达诺维奇                  |   2.03 | A            |
| 多曼塔斯-萨博尼斯                  |   2.11 | A            |
| 迈尔斯-特纳                        |   2.11 | A            |
| 赛迪斯-杨                          |   2.03 | A            |
| 达伦-科里森                        |   1.83 | C            |
| 韦斯利-马修斯                      |   1.96 | B            |
| 泰瑞克-埃文斯                      |   1.98 | B            |
| 道格-迈克德莫特                    |   2.03 | A            |
| 科里-约瑟夫                        |   1.91 | B            |
| 阿龙-霍勒迪                        |   1.85 | C            |
| TJ-利夫                            |   2.08 | A            |
| 凯尔-奥奎因                        |   2.08 | A            |
| 埃德蒙-萨姆纳                      |   1.96 | B            |
| 达文-里德                          |   1.98 | B            |
| 阿利兹-约翰逊                      |   2.06 | A            |
| 伊凯·阿尼博古                      |   2.08 | A            |
+------------------------------------+--------+--------------+
37 rows in set (0.00 sec)
```
**一般来说在 SQL99 中，我们需要连接的表会采用 JOIN 进行连接，ON 指定了连接条件，后面可以是等值连接，也可以采用非等值连接。**

#### USING 连接
当我们进行连接的时候，可以用 USING 指定数据表里的同名字段进行等值连接。
```
mysql> SELECT player_id, team_id, player_name, height, team_name FROM player JOIN team USING(team_id);
+-----------+---------+------------------------------------+--------+-----------------------+
| player_id | team_id | player_name                        | height | team_name             |
+-----------+---------+------------------------------------+--------+-----------------------+
|     10001 |    1001 | 韦恩-艾灵顿                        |   1.93 | 底特律活塞            |
|     10002 |    1001 | 雷吉-杰克逊                        |   1.91 | 底特律活塞            |
|     10003 |    1001 | 安德烈-德拉蒙德                    |   2.11 | 底特律活塞            |
|     10004 |    1001 | 索恩-马克                          |   2.16 | 底特律活塞            |
|     10005 |    1001 | 布鲁斯-布朗                        |   1.96 | 底特律活塞            |
|     10006 |    1001 | 兰斯顿-加洛韦                      |   1.88 | 底特律活塞            |
|     10007 |    1001 | 格伦-罗宾逊三世                    |   1.98 | 底特律活塞            |
|     10008 |    1001 | 伊斯梅尔-史密斯                    |   1.83 | 底特律活塞            |
|     10009 |    1001 | 扎扎-帕楚里亚                      |   2.11 | 底特律活塞            |
|     10010 |    1001 | 乔恩-洛伊尔                        |   2.08 | 底特律活塞            |
|     10011 |    1001 | 布雷克-格里芬                      |   2.08 | 底特律活塞            |
|     10012 |    1001 | 雷吉-巴洛克                        |   2.01 | 底特律活塞            |
|     10013 |    1001 | 卢克-肯纳德                        |   1.96 | 底特律活塞            |
|     10014 |    1001 | 斯坦利-约翰逊                      |   2.01 | 底特律活塞            |
|     10015 |    1001 | 亨利-埃伦森                        |   2.11 | 底特律活塞            |
|     10016 |    1001 | 凯里-托马斯                        |   1.91 | 底特律活塞            |
|     10017 |    1001 | 何塞-卡尔德隆                      |   1.91 | 底特律活塞            |
|     10018 |    1001 | 斯维亚托斯拉夫-米凯卢克            |   2.03 | 底特律活塞            |
|     10019 |    1001 | 扎克-洛夫顿                        |   1.93 | 底特律活塞            |
|     10020 |    1001 | 卡林-卢卡斯                        |   1.85 | 底特律活塞            |
|     10021 |    1002 | 维克多-奥拉迪波                    |   1.93 | 印第安纳步行者        |
|     10022 |    1002 | 博扬-博格达诺维奇                  |   2.03 | 印第安纳步行者        |
|     10023 |    1002 | 多曼塔斯-萨博尼斯                  |   2.11 | 印第安纳步行者        |
|     10024 |    1002 | 迈尔斯-特纳                        |   2.11 | 印第安纳步行者        |
|     10025 |    1002 | 赛迪斯-杨                          |   2.03 | 印第安纳步行者        |
|     10026 |    1002 | 达伦-科里森                        |   1.83 | 印第安纳步行者        |
|     10027 |    1002 | 韦斯利-马修斯                      |   1.96 | 印第安纳步行者        |
|     10028 |    1002 | 泰瑞克-埃文斯                      |   1.98 | 印第安纳步行者        |
|     10029 |    1002 | 道格-迈克德莫特                    |   2.03 | 印第安纳步行者        |
|     10030 |    1002 | 科里-约瑟夫                        |   1.91 | 印第安纳步行者        |
|     10031 |    1002 | 阿龙-霍勒迪                        |   1.85 | 印第安纳步行者        |
|     10032 |    1002 | TJ-利夫                            |   2.08 | 印第安纳步行者        |
|     10033 |    1002 | 凯尔-奥奎因                        |   2.08 | 印第安纳步行者        |
|     10034 |    1002 | 埃德蒙-萨姆纳                      |   1.96 | 印第安纳步行者        |
|     10035 |    1002 | 达文-里德                          |   1.98 | 印第安纳步行者        |
|     10036 |    1002 | 阿利兹-约翰逊                      |   2.06 | 印第安纳步行者        |
|     10037 |    1002 | 伊凯·阿尼博古                      |   2.08 | 印第安纳步行者        |
+-----------+---------+------------------------------------+--------+-----------------------+
37 rows in set (0.00 sec)
```
与自然连接 NATURAL JOIN 不同的是，USING 指定了具体的相同的字段名称，你需要在 USING 的括号 () 中填入要指定的同名字段。同时使用 JOIN USING 可以简化 JOIN ON 的等值连接，它与下面的 SQL 查询结果是相同的：
```
SELECT player_id, player.team_id, player_name, height, team_name FROM player JOIN team ON player.team_id = team.team_id
```
#### 外连接
SQL99 的外连接包括了三种形式：
1. 左外连接：LEFT JOIN 或 LEFT OUTER JOIN
2. 右外连接：RIGHT JOIN 或 RIGHT OUTER JOIN
3. 全外连接：FULL JOIN 或 FULL OUTER JOIN

全外连接实际上就是左外连接和右外连接的结合。在这三种外连接中，我们一般省略 OUTER 不写。

##### 1. 左外连接
SELECT * FROM player LEFT JOIN team ON player.team_id = team.team_id
##### 2. 右外连接
SELECT * FROM player RIGHT JOIN team ON player.team_id = team.team_id
##### 3. 全外连接
SELECT * FROM player FULL JOIN team ON player.team_id = team.team_id

MySQL 不支持全外连接，否则的话全外连接会返回左表和右表中的所有行。当表之间有匹配的行，会显示内连接的结果。当某行在另一个表中没有匹配时，那么会把另一个表中选择的列显示为空值。

也就是说，全外连接的结果 = 左右表匹配的数据 + 左表没有匹配到的数据 + 右表没有匹配到的数据。

#### 自连接
查看比布雷克·格里芬身高高的球员都有哪些<br>
**SQL99**
SELECT b.player_name, b.height FROM player as a JOIN player as b ON a.player_name = '布雷克-格里芬' and a.height < b.height;

#### SQL99 和 SQL92 的区别
连接操作基本上可以分成三种情况：
1. 内连接：将多个表之间满足连接条件的数据行查询出来。它包括了等值连接、非等值连接和自连接。
2. 外连接：会返回一个表中的所有记录，以及另一个表中匹配的行。它包括了左外连接、右外连接和全连接。
3. 交叉连接：也称为笛卡尔积，返回左表中每一行与右表中每一行的组合。在 SQL99 中使用的 CROSS JOIN。

SQL99 在 SQL92 的基础上提供了一些特殊语法，比如 NATURAL JOIN 和 JOIN USING。它们在实际中是比较常用的，省略了 ON 后面的等值条件判断，让 SQL 语句更加简洁。

#### 不同 DBMS 中使用连接需要注意的地方
**1. 不是所有的 DBMS 都支持全外连接**
虽然 SQL99 标准提供了全外连接，但不是所有的 DBMS 都支持。不仅 MySQL 不支持，Access、SQLite、MariaDB 等数据库软件也不支持。不过在 Oracle、DB2、SQL Server 中是支持的。

**2.Oracle 没有表别名 AS**
为了让 SQL 查询语句更简洁，我们经常会使用表别名 AS，不过在 Oracle 中是不存在 AS 的，使用表别名的时候，直接在表名后面写上表别名即可，比如 player p，而不是 player AS p。

**3.SQLite 的外连接只有左连接**
SQLite 是一款轻量级的数据库软件，在外连接上只支持左连接，不支持右连接，不过如果你想使用右连接的方式，比如table1 RIGHT JOIN table2，在 SQLite 你可以写成table2 LEFT JOIN table1，这样就可以得到相同的效果。

##### 关于连接的性能问题
**1. 控制连接表的数量**
多表连接就相当于嵌套 for 循环一样，非常消耗资源，会让 SQL 查询性能下降得很严重，因此不要连接不必要的表。在许多 DBMS 中，也都会有最大连接表的限制。

**2. 在连接时不要忘记 WHERE 语句**
多表连接的目的不是为了做笛卡尔积，而是筛选符合条件的数据行，因此在多表连接的时候不要忘记了 WHERE 语句，这样可以过滤掉不必要的数据行返回。

**3. 使用自连接而不是子查询**
我们在查看比布雷克·格里芬高的球员都有谁的时候，可以使用子查询，也可以使用自连接。一般情况建议你使用自连接，因为在许多 DBMS 的处理过程中，对于自连接的处理速度要比子查询快得多。你可以这样理解：子查询实际上是通过未知表进行查询后的条件判断，而自连接是通过已知的自身数据表进行条件判断，因此在大部分 DBMS 中都对自连接处理进行了优化。

在我们需要进行外连接的时候，建议采用 SQL99 标准，这样更适合阅读。

#### test
查询不同身高级别（对应 height_grades 表）对应的球员数量（对应 player 表）。
```
select h.height_level,count(p.player_id) num
from height_grades h
left join player p
on p.height
BETWEEN h.height_lowest and height_highest
group by height_level;

mysql> select h.height_level,count(p.player_id) num
    -> from height_grades h
    -> left join player p
    -> on p.height
    -> BETWEEN h.height_lowest and height_highest
    -> group by height_level;
+--------------+-----+
| height_level | num |
+--------------+-----+
| A            |  18 |
| B            |  14 |
| C            |   5 |
| D            |   0 |
+--------------+-----+
4 rows in set (0.00 sec)
```

#### 评论
完整的SELECT语句内部执行顺序是：
1. FROM子句组装数据（包括通过ON进行连接）
2. WHERE子句进行条件筛选
3. GROUP BY分组
4. 使用聚集函数进行计算；
5. HAVING筛选分组；
6. 计算所有的表达式；
7. SELECT 的字段；
8. ORDER BY排序
9. LIMIT筛选

