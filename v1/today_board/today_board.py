# Today Board
import copy
import json
import uuid
from typing import List

from fastapi import Depends, APIRouter, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session

from . import *
from ..awskeys import s3, bucket_name
from ..models import get_db
from ..models.TodayBoard import TodayBoardModel
from ..models.user import UserModel
from ..util import get_user_from_db

router = APIRouter()


@router.post("/")
def create_board(keyword: str = Form(...), content: str = Form(None), img: List[UploadFile] = File([]),
                 db: Session = Depends(get_db),
                 user: UserModel = Depends(get_user_from_db)):
    for file in img:
        name = str(uuid.uuid4()) + ".png"
        s3.upload_fileobj(file.file, bucket_name, name, ExtraArgs={'ACL': 'public-read'})
        # UploadFile 객체의 filename atr에 uuid에서 할당받은 name을 저장시킨다.
        file.filename = name
    db_board = TodayBoardModel(keyword=keyword, writer=user.id, content=content, image=img[0].filename if img else None)

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


@router.get("/")
def get_board_pagination(keyword: str, page: int, limit: int = 20, user: UserModel = Depends(get_user_from_db),
                         db: Session = Depends(get_db)):
    a = db.query(TodayBoardModel).filter(TodayBoardModel.keyword == keyword).offset(limit * (page - 1)).limit(
        limit).all()
    for i in a:
        if i.writer == user.id:
            i.__dict__["my_board"] = True
        else:
            i.__dict__["my_board"] = False
        [i].append(i.user)
        i.like = len(json.loads(i.like))
    return a


@router.put("/{index}")
def update_board(index: int, content: Optional[str] = Form(None), img: Optional[List[UploadFile]] = File([]),
                 user: UserModel = Depends(get_user_from_db),
                 db: Session = Depends(get_db)):
    db_board = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_board is None:
        raise HTTPException(status_code=404, detail="board not found")
    if db_board.user.id != user.id:
        raise HTTPException(status_code=404, detail="user not matched")

    if db_board.image:
        # s3에서 파일 삭제
        s3.delete_object(Bucket=bucket_name, Key=db_board.image)

    if img:
        for file in img:
            name = str(uuid.uuid4()) + ".png"
            s3.upload_fileobj(file.file, bucket_name, name, ExtraArgs={'ACL': 'public-read'})
            # UploadFile 객체의 filename atr에 uuid에서 할당받은 name을 저장시킨다.
            file.filename = name
            db_board.image = img[0].filename

    db_board.content = content if content else db_board.content

    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    db_board.__dict__["user"] = db_board.user
    db_board.like = len(json.loads(db_board.like))

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
