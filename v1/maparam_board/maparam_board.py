# Maparam board
import copy
import json
import uuid
from typing import List

from fastapi import Depends, APIRouter, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.MaparamBoard import MaparamBoardModel
from ..models.MaparamMember import MaparamMemberModel
from ..models.user import UserModel
from ..util import get_user_from_db, s3, bucket_name

router = APIRouter()


@router.post("/")
def create_board(maparam_index: int = Form(...), content: str = Form(...), img: List[UploadFile] = File([]),
                 db: Session = Depends(get_db),
                 user: UserModel = Depends(get_user_from_db)):

    chk_member = db.query(MaparamMemberModel).filter(
        (MaparamMemberModel.maparam_index == maparam_index) & (MaparamMemberModel.user_id == user.id))
    if not chk_member:
        raise HTTPException(status_code=404, detail="member not this group member")

    for file in img:
        name = str(uuid.uuid4()) + ".png"
        s3.upload_fileobj(file.file, bucket_name, name, ExtraArgs={'ACL': 'public-read'})
        # UploadFile 객체의 filename atr에 uuid에서 할당받은 name을 저장시킨다.
        file.filename = name

    db_board = MaparamBoardModel(maparam_index=maparam_index, writer=user.id,
                                 content=content, image=img[0].filename)
    db_board.like = "[]"

    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    db_board.__dict__["user"] = db_board.user
    db_board.like = len(json.loads(db_board.like))

    return db_board


@router.get("/{index}")
def get_board_by_index(index: int, db: Session = Depends(get_db)):
    db_board = db.query(MaparamBoardModel).filter(MaparamBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")
    return db_board


@router.get("/")
def get_board_pagination(maparam_name: str, page: int, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(MaparamBoardModel).filter(MaparamBoardModel.maparam_name == maparam_name).offset(
        limit * (page - 1)).limit(limit).all()


@router.put("/{index}")
def update_board(index: int, board: UpdateMaparamBoard, db: Session = Depends(get_db)):
    db_board = db.query(MaparamBoardModel).filter(MaparamBoardModel.index == index).one_or_none()
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
    db_board = db.query(MaparamBoardModel).filter(MaparamBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")
    a = copy.deepcopy(db_board.__dict__)
    db.delete(db_board)
    db.commit()
    return a


@router.get("/like/{index}")
def add_like(index: int, user_id: str, db: Session = Depends(get_db)):
    db_board = db.query(MaparamBoardModel).filter(MaparamBoardModel.index == index).one_or_none()
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
