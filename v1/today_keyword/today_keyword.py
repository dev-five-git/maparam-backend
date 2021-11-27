# Today Keyword

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.TodayKeyword import TodayKeywordModel

router = APIRouter()


@router.post("/")
def create_keyword(keyword: Keyword, db: Session = Depends(get_db)):
    keyword = TodayKeywordModel(keyword=keyword.keyword, date=keyword.date)
    db.add(keyword)
    db.commit()
    db.refresh(keyword)
    return keyword


@router.get("/")
def get_keyword_all(db: Session = Depends(get_db)):
    db_keyword = db.query(TodayKeywordModel).all()
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="keyword not found")
    return db_keyword


@router.delete("/{keyword}")
def delete_user_by_keyword(keyword: str, db: Session = Depends(get_db)):
    db_keyword = db.query(TodayKeywordModel).filter(TodayKeywordModel.keyword == keyword).one_or_none()
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="keyword is None")
    db.query(TodayKeywordModel).filter(TodayKeywordModel.keyword == keyword).delete()
    db.commit()
    return keyword
