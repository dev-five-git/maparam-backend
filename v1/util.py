from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session

from v1.models import get_db
from v1.models.user import UserModel


# 유저 가져오기
def get_user_from_db(token: str = Header(...), db: Session = Depends(get_db)):
    return get_user(db, token)


def get_user(db: Session, token: str):
    user = db.query(UserModel).filter(UserModel.id == token).one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="로그인 토큰에 문제가 있습니다.")
    return user

# 내가 쓴 게시물 확인
