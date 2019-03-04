from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/mogudb?charset=utf8", max_overflow=5,encoding='utf-8')
Base = declarative_base()


class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, autoincrement=True)    # 主键自增
    title = Column(String(128))
    img = Column(String(1024))
    price = Column(String(32))
    sku = Column(String(32))
    detail = Column(String(1024))