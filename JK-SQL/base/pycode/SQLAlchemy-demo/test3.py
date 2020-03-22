#-*- coding:utf-8 -*-
# author:cjx
# datetime:2020/3/21 18:02

from sqlalchemy import Column, String, Integer, Float, create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:123456@bigdata-pro01:3306/chenyang')


class Player(Base):
    __tablename__ = 'player'

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer)
    player_name = Column(String(255))
    height = Column(Float(3, 2))


def to_dict(self):
    return {c.name: getattr(self, c.name, None)
            for c in self.__table__.columns}


if __name__ == '__main__':
    DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.to_dict = to_dict
print("更新前:")
rows = session.query(Player).filter(Player.height == 2.08).all()
print([row.to_dict() for row in rows])
# 参考: https://docs.sqlalchemy.org/en/13/core/dml.html#sqlalchemy.sql.expression.update
stmt = update(Player).where(Player.height == 2.08).values(height=2.09)
engine.execute(stmt)
session.commit()
rows = session.query(Player).filter(Player.height == 2.09).all()
print("更新后:")
print([row.to_dict() for row in rows])
session.close()