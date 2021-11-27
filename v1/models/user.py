from sqlalchemy import Column, String, DateTime, func, Integer, Text

from database import Base
from database import engine


class UserModel(Base):
    __tablename__ = 'user'
    id = Column(String(16), primary_key=True)
    name = Column(String(10))
    pw = Column(String(64))
    email = Column(String(50))
    age = Column(Integer)
    hashtag = Column(Text)
    created_at = Column(DateTime, default=func.now())
    introduce = Column(Text)
    profile_img = Column(Text)


UserModel.__table__.create(bind=engine, checkfirst=True)
