# -*- coding:utf-8 -*-
from sqlalchemy import and_
from sqlalchemy import Column, INT, FLOAT, VARCHAR
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Test_db:
    def __init__(self):
        """此处填上自己的连接配置"""
        self.engine = create_engine(
            'mysql+pymysql://root:123456@bigdata-pro01:3306/chenyang?charset=utf8')
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def update(self, target_class, query_filter, target_obj):
        """
        更新操作通用方法
        :param target_class: 表对象
        :param query_filter: 查询条件
        :param target_obj: 更新目标对象
        :return:
        """
        try:
            self.session.query(target_class).filter(query_filter).update(target_obj)
            self.session.commit()
            self.session.close()
            return True
        except Exception as e:
            print(e)


class Player(Base):
    """定义表结构"""
    __tablename__ = 'player'
    player_id = Column(INT(), primary_key=True)
    team_id = Column(INT())
    player_name = Column(VARCHAR(255))
    height = Column(FLOAT())

    def __init__(self, player_id, team_id, player_name, height):
        self.player_id = player_id
        self.team_id = team_id
        self.player_name = player_name
        self.height = height


if __name__ == '__main__':
    db_obj = Test_db()
    query_filter = and_(Player.height == 2.08)
    target_obj = {'height': 2.09}
    update_result = db_obj.update(Player, query_filter, target_obj)