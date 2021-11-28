from sqlalchemy import Column, String, Integer, ForeignKey, Text, func, DateTime
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from .MaparamNotice import MaparamNoticeModel
from .user import UserModel


class MaparamNoticeCommentModel(Base):
    __tablename__ = 'maparam_notice_comment'
    index = Column(Integer, primary_key=True, autoincrement=True)
    board_index = Column(Integer, ForeignKey('maparam_notice.index'))
    writer = Column(String(16), ForeignKey('user.id'))
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship(UserModel, backref=backref("maparam_notice_comment", cascade="all,delete"))
    board = relationship(MaparamNoticeModel, backref=backref("maparam_notice_comment", cascade="all,delete"))


MaparamNoticeCommentModel.__table__.create(bind=engine, checkfirst=True)
