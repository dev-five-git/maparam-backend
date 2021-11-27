from sqlalchemy import Column, String, DateTime, func, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from v1.models.user import UserModel


class MaparamModel(Base):
    __tablename__ = 'maparam'
    index = Column(Integer, primary_key=True, autoincrement=True)
    creater_id = Column(String(16), ForeignKey('user.id'))
    name = Column(String(20), unique=True)
    max_member_size = Column(Integer)
    introduce = Column(Text)
    created_at = Column(DateTime, default=func.now())

    user = relationship(UserModel, backref=backref("maparam", cascade="all,delete"))


MaparamModel.__table__.create(bind=engine, checkfirst=True)
