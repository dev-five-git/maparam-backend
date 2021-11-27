# User
import uuid
from typing import List

import boto3 as boto3
from fastapi import Depends, APIRouter, HTTPException, Body, UploadFile, File
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.user import UserModel

router = APIRouter()

s3 = boto3.client('s3', aws_access_key_id='AKIAYVJ7YJKE5N2FJGML',
                  aws_secret_access_key='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',
                  )
bucket_name = 'maparam'


# @router.get("/page", dependencies=[Depends(check_admin)])
# def read_user_by_page(page: int, limit: int, db: Session = Depends(get_db)):
#     db_viagallery_count = db.query(UserModel).count()
#     return {"count": db_viagallery_count,
#             "list": db.query(UserModel).offset(limit * (page - 1)).limit(limit).all()}


@router.post("/create")
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user.id).one_or_none()
    if db_user:
        raise HTTPException(status_code=400, detail="id already registered")

    db_user_email = db.query(UserModel).filter(UserModel.email == user.email).one_or_none()
    if db_user_email:
        raise HTTPException(status_code=400, detail="already registered with this email")

    db_user = UserModel(id=user.id, name=user.name, pw=user.pw,
                        age=user.age, email=user.email, hashtag=user.hashtag)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    del db_user.__dict__["pw"]
    return db_user


@router.get("/{user_id}")
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    del db_user.__dict__["pw"]
    return db_user


@router.get("/id/", response_model=UserId)
def get_id_by_name_and_email(name: str, email: str, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter((UserModel.name == name) & (UserModel.email == email)).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User_id not found")
    return db_user.__dict__


@router.get("/pw/", response_model=UserPw)
def read_pw_by_name_and_email_and_id(name: str, id: str, email: str, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(
        (UserModel.name == name) & (UserModel.email == email) & (UserModel.id == id)).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User_id not found")
    return db_user.__dict__


@router.put("/{user_id}")
def update_user(user_id: str, user: UpdateUser, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User_id not found")

    for var, value in vars(user).items():
        # if var == 'pw':
        #     setattr(db_user, var, hashlib.sha256(value.encode()).hexdigest()) if value else None
        setattr(db_user, var, value) if value else None

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    del db_user.__dict__["pw"]
    return db_user


@router.delete("/{user_id}")
def delete_user_by_id(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="id is None")
    db.query(UserModel).filter(UserModel.id == user_id).delete()
    db.commit()
    return db_user


@router.post("/{user_id}/introduce")
def add_user_introduce(user_id: str, intro: str = Body(...), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="id is None")
    db_user.introduce = intro
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    del db_user.__dict__["pw"]
    return db_user


@router.post("/{user_id}/profileimg")
def add_user_profileimg(user_id: str, img: List[UploadFile] = File([]), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="id is None")
    # 이미지파일 서버로 전송
    for file in img:
        name = str(uuid.uuid4()) + ".png"
        s3.upload_fileobj(file.file, bucket_name, name, ExtraArgs={'ACL': 'public-read'})
        # UploadFile 객체의 filename atr에 uuid에서 할당받은 name을 저장시킨다.
        file.filename = name
    db_user.profile_img = img[0].filename


    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    del db_user.__dict__["pw"]
    return db_user
