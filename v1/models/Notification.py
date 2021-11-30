from sqlalchemy import Column, String, DateTime, func, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from database import Base
from database import engine
from v1.models.user import UserModel


class NotificationModel(Base):
    __tablename__ = 'notification'
    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(16), ForeignKey('user.id'))
    from_where = Column(String(30))
    from_who = Column(String(10))  # 닉네임 으로 저장
    checked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship(UserModel, backref=backref("notification", cascade="all,delete"))


NotificationModel.__table__.create(bind=engine, checkfirst=True)
