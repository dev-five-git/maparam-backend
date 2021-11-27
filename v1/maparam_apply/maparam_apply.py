# Maparam Member

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.MaparamApply import MaparamApplyModel
from ..models.MaparamMember import MaparamMemberModel

router = APIRouter()


@router.post("/")
def create_maparam_apply(apply: MaparamApply, db: Session = Depends(get_db)):
    db_apply = MaparamApplyModel(user_id=apply.user_id, maparam=apply.maparam, status=0)
    db.add(db_apply)
    db.commit()
    db.refresh(db_apply)
    return db_apply


@router.get("/{maparam_name}")
def get_apply_by_maparam(maparam_name: str, db: Session = Depends(get_db)):
    db_apply = db.query(MaparamApplyModel).filter(MaparamApplyModel.maparam == maparam_name).all()
    if db_apply is None:
        raise HTTPException(status_code=404, detail="apply not found")
    return db_apply


@router.put("/{index}")
def check_maparam_member_by_manager(index: int, status: ApplyCheck, db: Session = Depends(get_db)):
    db_apply = db.query(MaparamApplyModel).filter(MaparamApplyModel.index == index).one_or_none()
    if db_apply is None:
        raise HTTPException(status_code=404, detail="apply not found")
    if status.status == 1:
        member = db_apply.user
        chk_user = db.query(MaparamMemberModel).filter(
            (MaparamMemberModel.user_id == member.id) & (
                    MaparamMemberModel.maparam == db_apply.maparam)).one_or_none()
        if chk_user:
            raise HTTPException(status_code=404, detail="user already joined")
        db_member = MaparamMemberModel(user_id=member.id, maparam=db_apply.maparam, tier=1)
        db.add(db_member)

    db_apply.status = status.status
    db.add(db_apply)
    db.commit()
    db.refresh(db_member)
    return db_member
