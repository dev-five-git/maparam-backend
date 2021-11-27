from sqlalchemy import Column, String, Integer, Date

from database import Base
from database import engine


class TodayKeywordModel(Base):
    __tablename__ = 'today_keyword'
    index = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(10), unique=True)
    date = Column(Date, unique=True)


TodayKeywordModel.__table__.create(bind=engine, checkfirst=True)
