# Timeline board
import copy
import json

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.TimelineBoard import TimelineBoardModel

router = APIRouter()


@router.post("/")
def create_board(board: TimelineBoard, db: Session = Depends(get_db)):
    db_board = TimelineBoardModel(location_latitude=board.location_latitude,
                                  location_longitude=board.location_longitude, writer=board.writer,
                                  content=board.content, image=board.image)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


@router.get("/{index}")
def get_board_by_index(index: int, db: Session = Depends(get_db)):
    db_board = db.query(TimelineBoardModel).filter(TimelineBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")
    return db_board


@router.get("/")
def get_board_pagination(page: int, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(TimelineBoardModel).offset(limit * (page - 1)).limit(limit).all()


@router.put("/{index}")
def update_board(index: int, board: UpdateTimelineBoard, db: Session = Depends(get_db)):
    db_board = db.query(TimelineBoardModel).filter(TimelineBoardModel.index == index).one_or_none()
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
    db_board = db.query(TimelineBoardModel).filter(TimelineBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")
    a = copy.deepcopy(db_board.__dict__)
    db.delete(db_board)
    db.commit()
    return a


@router.get("/like/{index}")
def add_like(index: int, user_id: str, db: Session = Depends(get_db)):
    db_board = db.query(TimelineBoardModel).filter(TimelineBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")
    if db_board.like:
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

    else:
        like_list = [user_id]
        a = "좋아요 +"
        db_board.like = json.dumps(like_list)
        db.add(db_board)
        db.commit()

    return a


@router.post("/gps")
def get_board_by_location(location: CurrentLocation, distance: int, db: Session = Depends(get_db)):
    distance = distance / 1000
    latitude = 0.00893655 * distance
    longitude = 0.01065076 * distance
    location_latitude = location.location_latitude
    location_longitude = location.location_longitude
    return db.query(TimelineBoardModel).filter(
        (location_latitude - latitude <= TimelineBoardModel.location_latitude) & (
                TimelineBoardModel.location_latitude <= location_latitude + latitude) & (
                location_longitude - longitude <= TimelineBoardModel.location_longitude) & (
                TimelineBoardModel.location_longitude <= location_longitude + longitude)).all()
