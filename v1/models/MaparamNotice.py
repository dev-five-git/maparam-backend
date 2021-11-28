from sqlalchemy import Column, String, DateTime, func, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from v1.models.Maparam import MaparamModel
from v1.models.user import UserModel


class MaparamNoticeModel(Base):
    __tablename__ = 'maparam_notice'
    index = Column(Integer, primary_key=True, autoincrement=True)
    maparam_index = Column(Integer, ForeignKey('maparam.index'))
    writer = Column(String(16), ForeignKey('user.id'))
    content = Column(Text)
    image = Column(Text)
    like = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship(UserModel, backref=backref("maparam_notice", cascade="all,delete"))
    maparam = relationship(MaparamModel, backref=backref("maparam_notice", cascade="all,delete"))


MaparamNoticeModel.__table__.create(bind=engine, checkfirst=True)
