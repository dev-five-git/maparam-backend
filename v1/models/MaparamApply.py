from sqlalchemy import Column, String, Integer, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from .Maparam import MaparamModel
from .user import UserModel


class MaparamApplyModel(Base):
    __tablename__ = 'maparam_apply'
    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(16), ForeignKey('user.id'))
    maparam_index = Column(Integer, ForeignKey('maparam.index'))
    status = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    user = relationship(UserModel, backref=backref("maparam_apply", cascade="all,delete"))
    maparam = relationship(MaparamModel, backref=backref("maparam_apply", cascade="all,delete"))


MaparamApplyModel.__table__.create(bind=engine, checkfirst=True)
