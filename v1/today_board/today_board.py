# Community
import copy

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.TodayBoard import TodayBoardModel

router = APIRouter()


@router.post("/")
def create_board(board: TodayBoard, db: Session = Depends(get_db)):
    db_board = TodayBoardModel(keyword=board.keyword, writer=board.writer, content=board.content, image=board.image)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


@router.get("/{index}")
def get_board_by_index(index: int, db: Session = Depends(get_db)):
    db_community = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_community is None:
        raise HTTPException(status_code=404, detail="Community not found")
    return db_community


@router.get("/")
def get_community_pagination(page: int, db: Session = Depends(get_db)):
    return db.query(TodayBoardModel).offset(20 * (page - 1)).limit(20).all()


@router.put("/{index}")
def update_community(index: int, community: UpdateTodayBoard, db: Session = Depends(get_db)):
    db_community = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_community is None:
        raise HTTPException(status_code=404, detail="Community not found")

    for var, value in vars(community).items():
        setattr(db_community, var, value) if value else None

    db.add(db_community)
    db.commit()
    db.refresh(db_community)
    return db_community


@router.delete("/{index}")
def delete_community(index: int, db: Session = Depends(get_db)):
    db_community = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_community is None:
        raise HTTPException(status_code=404, detail="Community not found")
    a = copy.deepcopy(db_community.__dict__)
    db.delete(db_community)
    db.commit()
    return a
