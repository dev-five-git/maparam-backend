from sqlalchemy import Column, String, DateTime, func, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from v1.models.TodayKeyword import TodayKeywordModel
from v1.models.user import UserModel


class TodayBoardModel(Base):
    __tablename__ = 'today_board'
    index = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(10), ForeignKey('today_keyword.keyword'))
    writer = Column(String(16), ForeignKey('user.id'))
    content = Column(Text)
    image = Column(Text)
    like = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship(UserModel, backref=backref("today_board", cascade="all,delete"))
    keyword_set = relationship(TodayKeywordModel, backref=backref("today_board"))


TodayBoardModel.__table__.create(bind=engine, checkfirst=True)
