from sqlalchemy import Column, String, Integer, ForeignKey, Text, func, DateTime
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from .MaparamBoard import MaparamBoardModel
from .user import UserModel


class MaparamBoardCommentModel(Base):
    __tablename__ = 'maparam_board_comment'
    index = Column(Integer, primary_key=True, autoincrement=True)
    board_index = Column(Integer, ForeignKey('maparam_board.index'))
    writer = Column(String(16), ForeignKey('user.id'))
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship(UserModel, backref=backref("maparam_board_comment", cascade="all,delete"))
    board = relationship(MaparamBoardModel, backref=backref("maparam_board_comment", cascade="all,delete"))


MaparamBoardCommentModel.__table__.create(bind=engine, checkfirst=True)
