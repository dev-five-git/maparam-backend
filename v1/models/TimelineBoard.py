from sqlalchemy import Column, String, DateTime, func, Integer, Text, ForeignKey, Float, Numeric
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from v1.models.user import UserModel


class TimelineBoardModel(Base):
    __tablename__ = 'timeline_board'
    index = Column(Integer, primary_key=True, autoincrement=True)
    location_latitude = Column(Numeric(precision=10, scale=8))
    location_longitude = Column(Numeric(precision=11, scale=8))
    writer = Column(String(16), ForeignKey('user.id'))
    content = Column(Text)
    image = Column(Text)
    hashtag = Column(Text)
    like = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship(UserModel, backref=backref("timeline_board", cascade="all,delete"))


TimelineBoardModel.__table__.create(bind=engine, checkfirst=True)
