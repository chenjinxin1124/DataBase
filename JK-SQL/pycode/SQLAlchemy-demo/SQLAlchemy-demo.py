#-*- coding:utf-8 -*-
# author:cjx
# datetime:2020/3/21 16:04

'''
采用 ORM 也会付出一些代价，比如性能上的一些损失.
面对一些复杂的数据查询，ORM 会显得力不从心。
虽然可以实现功能，但相比于直接编写 SQL 查询语句来说，ORM 需要编写的代码量和花费的时间会比较多，
这种情况下，直接编写 SQL 反而会更简单有效。
'''

# Python 的三种主流的 ORM 框架：
# Django：是 Python 的 WEB 应用开发框架，本身走大而全的方式。Django 采用了 MTV 的框架模式，包括了 Model（模型），View（视图）和 Template（模版）。Model 模型只是 Django 的一部分功能，我们可以通过它来实现数据库的增删改查操作。
# SQLALchemy：是 Python 中常用的 ORM 框架之一。它提供了 SQL 工具包及 ORM 工具，如果你想用支持 ORM 和支持原生 SQL 两种方式的工具，那么 SQLALchemy 是很好的选择。另外 SQLALchemy 的社区更加活跃，这对项目实施会很有帮助。
# peewee：是一个轻量级的 ORM 框架，简单易用。peewee 采用了 Model 类、Field 实例和 Model 实例来与数据库建立映射关系，从而完成面向对象的管理方式。使用起来方便，学习成本也低。

# 使用 SQLAlchemy 来操作 MySQL

from sqlalchemy import create_engine
# 使用相应的数据类型，需要提前在 SQLAlchemy 中引用
from sqlalchemy import Column, String, Integer, Float

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 初始化数据库连接，修改为你的数据库用户名和密码
engine = create_engine('mysql+mysqlconnector://root:123456@bigdata-pro01:3306/chenyang')

# 创建对象的基类:
Base = declarative_base()
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 创建模型

# 定义Player对象:
class Player(Base):
    # __tablename__ 指明了模型对应的数据表名称，即 player 数据表。
    # 表的名字:
    __tablename__ = 'player'

    # 采用 Column
    # 创建列约束:primary_key、autoincrement、default、unique
    # 表的结构:
    player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    player_name = Column(String(255))
    height = Column(Float(3, 2))

    # 对数据表进行增删改查
    # 给 player 表增加一名新球员，姓名为“约翰·科林斯”，球队 ID 为 1003（即亚特兰大老鹰），身高为 2.08。

def add_player():
    # 初始化 DBSession，相当于创建一个数据库的会话实例 session。
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    session = DBSession()


    # 创建Player对象:
    new_player = Player(team_id = 1003, player_name = "约翰-科林斯", height = 2.08)
    # 添加到session:
    session.add(new_player)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

def query_player():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # 如果我们想要在 Python 中对 query 结果进行打印，可以对 Base 类增加to_dict()方法，相当于将对象转化成了 Python 的字典类型。
    # 增加to_dict()方法到Base类中
    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}

    # 将对象可以转化为dict类型
    Base.to_dict = to_dict
    # 查询身高>=2.08的球员有哪些
    # 在进行查询的时候，我们使用的是 filter 方法，对应的是 SQL 中的 WHERE 条件查询。除此之外，filter 也支持多条件查询。
    '''
    如果是 AND 的关系，比如我们想要查询身高 ≥ 2.08，同时身高 ≤ 2.10 的球员，可以写成下面这样：
    rows = session.query(Player).filter(Player.height >=2.08, Player.height <=2.10).all()
    如果是 OR 的关系，比如我们想要查询身高 ≥ 2.08，或者身高 ≤ 2.10 的球员，可以写成这样：
    这里我们使用了 SQLAlchemy 的 or_ 操作符，在使用它之前你需要进行引入，即：from sqlalchemy import or_。
    rows = session.query(Player).filter(or_(Player.height >=2.08, Player.height <=2.10)).all()
    '''
    rows = session.query(Player).filter(Player.height >= 2.08).all()
    print([row.to_dict() for row in rows])

    # SQLAlchemy 也同样支持分组操作、排序和返回指定数量的结果。
    # 比如我想要按照 team_id 进行分组，同时筛选分组后数据行数大于 5 的分组，并且按照分组后数据行数递增的顺序进行排序，显示 team_id 字段，以及每个分组的数据行数。那么代码如下：
    from sqlalchemy import func
    rows = session.query(Player.team_id, func.count(Player.player_id)).group_by(Player.team_id).having(
        func.count(Player.player_id) > 5).order_by(func.count(Player.player_id).asc()).all()
    print(rows)
    '''
    注意：
    1. 我们把需要显示的字段 Player.team_id, func.count(Player.player_id) 作为 query 的参数，其中我们需要用到 sqlalchemy 的 func 类，
    它提供了各种聚集函数，比如 func.count 函数。
    2. 在 query() 后面使用了 group_by() 进行分组，参数设置为 Player.team_id 字段，再使用 having 对分组条件进行筛选，参数为func.count(Player.player_id)>5。
    3. 使用 order_by 进行排序，参数为func.count(Player.player_id).asc()，也就是按照分组后的数据行数递增的顺序进行排序，最后使用.all() 方法需要返回全部的数据。
    '''

    session.close()

def delete_player():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    '''
    删除姓名为约翰·科林斯的球员，首先我们需要进行查询，然后从 session 对象中进行删除，最后进行 commit 提交
    需要说明的是，判断球员姓名是否为约翰·科林斯，这里需要使用（==）。
    '''
    row = session.query(Player).filter(Player.player_name == '约翰-科林斯').first()
    session.delete(row)
    session.commit()

    session.close()

def updata_player():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # 修改某条数据，也需要进行查询，然后再进行修改。比如我想把球员索恩·马克的身高改成 2.17，那么执行完之后直接对 session 对象进行 commit 操作
    row = session.query(Player).filter(Player.player_name == '索恩-马克').first()
    row.height = 2.17
    session.commit()
    session.close()

    session.close()
if __name__ == '__main__':
    # add
    # add_player()
    # query
    # query_player()
    # delete
    # delete_player()
    # updata
    updata_player()
