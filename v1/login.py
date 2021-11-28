# Login

from fastapi import Depends, HTTPException, Body
from sqlalchemy.orm import Session

from . import *
from .models import get_db
from .models.user import UserModel

router = APIRouter()


@router.post("/login")
def login(id: str = Body(...), pw: str = Body(...), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == id).one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="id not exist")
    if db_user.pw != pw:
        raise HTTPException(status_code=404, detail="pw not match")
    return db_user
