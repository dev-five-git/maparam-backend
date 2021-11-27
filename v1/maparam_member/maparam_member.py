# Maparam Member
import copy

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.MaparamMember import MaparamMemberModel

router = APIRouter()


@router.post("/")
def create_maparam_member(member: MaparamMember, db: Session = Depends(get_db)):
    db_member = MaparamMemberModel(user_id=member.user_id, maparam=member.maparam, tier=member.tier)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/{maparam_name}")
def get_member_by_maparam(maparam_name: str, db: Session = Depends(get_db)):
    db_member = db.query(MaparamMemberModel).filter(MaparamMemberModel.maparam == maparam_name).all()
    if db_member is None:
        raise HTTPException(status_code=404, detail="member not found")
    return db_member


@router.put("/{index}")
def update_maparam_member(index: int, member: UpdateMaparamMember, db: Session = Depends(get_db)):
    db_member = db.query(MaparamMemberModel).filter(MaparamMemberModel.index == index).one_or_none()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    for var, value in vars(member).items():
        setattr(db_member, var, value) if value else None

    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/{index}")
def delete_maparam_member(index: int, db: Session = Depends(get_db)):
    db_member = db.query(MaparamMemberModel).filter(MaparamMemberModel.index == index).one_or_none()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    a = copy.deepcopy(db_member.__dict__)
    db.delete(db_member)
    db.commit()
    return a
