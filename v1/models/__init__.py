from fastapi import APIRouter
from sqlalchemy.orm import Session

from database import session_local

v1_router = APIRouter()


def get_db() -> Session:
    db = session_local()
    try:
        yield db
    finally:
        db.close()
