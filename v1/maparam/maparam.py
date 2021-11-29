# Maparam
import copy

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.Maparam import MaparamModel
from ..models.MaparamMember import MaparamMemberModel

router = APIRouter()


@router.post("/")
def create_maparam(maparam: Maparam, db: Session = Depends(get_db)):
    db_maparam_search = db.query(MaparamModel).filter(MaparamModel.name == maparam.name).one_or_none()
    if db_maparam_search:
        raise HTTPException(status_code=404, detail="same name exist")
    db_maparam = MaparamModel(creater_id=maparam.creater_id, name=maparam.name, max_member_size=maparam.max_member_size,
                              introduce=maparam.introduce)
    db.add(db_maparam)
    db.commit()
    db.refresh(db_maparam)
    # 씨발 왜안되지...
    db_member = MaparamMemberModel(user_id=db_maparam.creater_id, maparam=db_maparam.index, tier=0)
    db.add(db_member)
    db.commit()
    return db_maparam


@router.get("/{index}")
def get_maparam_by_index(index: int, db: Session = Depends(get_db)):
    db_maparam = db.query(MaparamModel).filter(MaparamModel.index == index).one_or_none()
    if db_maparam is None:
        raise HTTPException(status_code=404, detail="maparam not found")
    return db_maparam


@router.put("/{index}")
def update_maparam(index: int, maparam: UpdateMaparam, db: Session = Depends(get_db)):
    db_maparam = db.query(MaparamModel).filter(MaparamModel.index == index).one_or_none()
    if db_maparam is None:
        raise HTTPException(status_code=404, detail="maparam not found")

    for var, value in vars(maparam).items():
        setattr(db_maparam, var, value) if value else None

    db.add(db_maparam)
    db.commit()
    db.refresh(db_maparam)
    return db_maparam


@router.delete("/{index}")
def delete_maparam(index: int, db: Session = Depends(get_db)):
    db_maparam = db.query(MaparamModel).filter(MaparamModel.index == index).one_or_none()
    if db_maparam is None:
        raise HTTPException(status_code=404, detail="maparam not found")
    a = copy.deepcopy(db_maparam.__dict__)
    db.delete(db_maparam)
    db.commit()
    return a
