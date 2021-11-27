from sqlalchemy import Column, String, Integer, ForeignKey, Text, func, DateTime
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from .TimelineBoard import TimelineBoardModel
from .user import UserModel


class TimelineCommentModel(Base):
    __tablename__ = 'timeline_board_comment'
    index = Column(Integer, primary_key=True, autoincrement=True)
    board_index = Column(Integer, ForeignKey('timeline_board.index'))
    writer = Column(String(16), ForeignKey('user.id'))
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship(UserModel, backref=backref("timeline_board_comment", cascade="all,delete"))
    board = relationship(TimelineBoardModel, backref=backref("timeline_board_comment", cascade="all,delete"))


TimelineCommentModel.__table__.create(bind=engine, checkfirst=True)
