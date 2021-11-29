# Today Board
import copy
import json

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.TodayBoard import TodayBoardModel
from ..models.user import UserModel
from ..util import get_user_from_db

router = APIRouter()


@router.post("/")
def create_board(board: TodayBoard, db: Session = Depends(get_db), user: UserModel = Depends(get_user_from_db)):
    db_board = TodayBoardModel(keyword=board.keyword, writer=user.id, content=board.content, image=board.image)
    db_board.like = "[]"
    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    db_board.__dict__["user"] = db_board.user
    db_board.like = len(json.loads(db_board.like))

    return db_board


@router.get("/{index}", dependencies=[Depends(get_user_from_db)])
def get_board_by_index(index: int, db: Session = Depends(get_db)):
    db_board = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")

    db_board.__dict__["user"] = db_board.user
    db_board.like = len(json.loads(db_board.like))

    return db_board


@router.get("/", dependencies=[Depends(get_user_from_db)])
def get_board_pagination(page: int, limit: int = 20, db: Session = Depends(get_db)):
    a = db.query(TodayBoardModel).offset(limit * (page - 1)).limit(limit).all()
    for i in a:
        [i].append(i.user)
        i.like = len(json.loads(i.like))
    return a


@router.put("/{index}")
def update_board(index: int, board: UpdateTodayBoard, db: Session = Depends(get_db)):
    db_board = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")

    for var, value in vars(board).items():
        setattr(db_board, var, value) if value else None

    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


@router.delete("/{index}")
def delete_board(index: int, db: Session = Depends(get_db)):
    db_board = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")
    a = copy.deepcopy(db_board.__dict__)
    db.delete(db_board)
    db.commit()
    return a


@router.get("/like/{index}")
def add_like(index: int, user_id: str, db: Session = Depends(get_db)):
    db_board = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")

    like_list = json.loads(db_board.like)
    if user_id not in like_list:
        like_list.append(user_id)
        a = "좋아요 +"
        db_board.like = json.dumps(like_list)
        db.add(db_board)
        db.commit()
    else:
        like_list.remove(user_id)
        a = "좋아요 -"
        db_board.like = json.dumps(like_list)
        db.add(db_board)
        db.commit()
    return a
