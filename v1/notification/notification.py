from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from v1.models import get_db
from v1.models.Notification import NotificationModel
from v1.models.user import UserModel
from v1.util import get_user_from_db

router = APIRouter()


@router.get("/")
def get_user_notification(user: UserModel = Depends(get_user_from_db), db: Session = Depends(get_db)):
    return {"noti_list": db.query(NotificationModel).filter(
        (NotificationModel.user_id == user.id) & (NotificationModel.checked == False)).all()}


@router.get("/{index}")
def check_notification(index: int, user: UserModel = Depends(get_user_from_db), db: Session = Depends(get_db)):
    noti = db.query(NotificationModel).filter(NotificationModel.index == index).one_or_none()
    noti.checked = True
    db.add(noti)
    db.commit()


@router.get("/allcheck/")
def get_user_notification_all_checked(user: UserModel = Depends(get_user_from_db), db: Session = Depends(get_db)):
    noti_list = db.query(NotificationModel).filter(
        (NotificationModel.user_id == user.id) & (NotificationModel.checked == False)).all()
    for i in noti_list:
        i.checked = True
    db.bulk_save_objects(noti_list)
    db.commit()


def create_noti(db: Session, user_id: str, from_where: str, from_who: str):
    noti = NotificationModel(user_id=user_id, from_where=from_where, from_who=from_who)
    db.add(noti)
    db.commit()
