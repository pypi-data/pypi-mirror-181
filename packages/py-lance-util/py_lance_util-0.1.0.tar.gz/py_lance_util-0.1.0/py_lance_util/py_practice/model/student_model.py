# 导入:
from sqlalchemy import Column, Integer, String, DateTime, create_engine

from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from urllib.parse import quote
from config.config import get_settings

settings = get_settings()
# 创建对象的基类:
Base = declarative_base()

# 定义User对象:


class student(Base):
    # 表的名字:
    __tablename__ = 'student'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String(20))


class t1(Base):
    __tablename__ = 't1'
    id = Column(Integer, primary_key=True)
    m_id = Column(Integer)
    name = Column(String(255))
    identity_no = Column(String(30))
    address = Column(String(255))
    create_time = Column(DateTime, default=datetime.now)
    modify_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)


# 创建所有模型对应的表
# DB_URI = "mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}".format(
#     username=settings.db_user,
#     password=quote(settings.db_passwd, '', "utf-8", None),
#     hostname=settings.db_host,
#     port=settings.db_port,
#     database=settings.db_name
# )
# engine = create_engine(DB_URI, echo=True)
# Base.metadata.create_all(engine)
