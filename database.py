from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://admin:devfive*@devfive-db.c76grlw09hns.ap-northeast-2.rds.amazonaws.com:3306/maparam'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
