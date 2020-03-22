#-*- coding:utf-8 -*-
# author:cjx
# datetime:2020/3/21 17:50

# 针对 player 数据表，使用 SQLAlalchemy 工具查询身高为 2.08 米的球员，并且将这些球员的身高修改为 2.09。

# 使用相应的数据类型，需要提前在 SQLAlchemy 中引用
from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 初始化数据库连接，修改为你的数据库用户名和密码
engine = create_engine('mysql+mysqlconnector://root:123456@bigdata-pro01:3306/chenyang')

# 创建对象的基类:
Base = declarative_base()
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

class Player(Base):
    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    player_name = Column(String(255))
    height = Column(Float(3, 2))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}

session = DBSession()

rows = session.query(Player).filter(Player.height == 2.08).all()
for i in rows:
    print([i.to_dict()])
    i.height = 2.09
    session.commit()

rows = session.query(Player).filter(Player.height == 2.09).all()
for i in rows:
    print([i.to_dict()])