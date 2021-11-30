# Maparam
import copy

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.Maparam import MaparamModel
from ..models.MaparamMember import MaparamMemberModel
from ..models.user import UserModel
from ..util import get_user_from_db

router = APIRouter()


@router.post("/")
def create_maparam(maparam: Maparam, db: Session = Depends(get_db)):
    db_maparam_search = db.query(MaparamModel).filter(MaparamModel.name == maparam.name).one_or_none()
    if db_maparam_search:
        raise HTTPException(status_code=404, detail="same name exist")

    db_maparam = MaparamModel(creater_id=maparam.creater_id, name=maparam.name, max_member_size=maparam.max_member_size,
                              introduce=maparam.introduce)
    db.add(db_maparam)
    db.flush()

    db_member = MaparamMemberModel(user_id=db_maparam.creater_id, maparam_index=db_maparam.index, tier=0)
    db.add(db_member)
    db.flush()

    db.commit()
    print(db_maparam.index)

    return db_maparam


@router.get("/{index}")
def get_maparam_by_index(index: int, user: UserModel = Depends(get_user_from_db), db: Session = Depends(get_db)):
    db_maparam = db.query(MaparamModel).filter(MaparamModel.index == index).one_or_none()
    if db_maparam is None:
        raise HTTPException(status_code=404, detail="maparam not found")
    chk_joined = db.query(MaparamMemberModel).filter((MaparamMemberModel.user_id == user.id) & (
            MaparamMemberModel.maparam_index == index)).one_or_none()
    if not chk_joined:
        db_maparam.__dict__["tier"] = None
    else:
        if chk_joined.tier == 0:
            db_maparam.__dict__["tier"] = 0
        else:
            db_maparam.__dict__["tier"] = 1
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


@router.get("/my/")
def get_my_maparam(user: UserModel = Depends(get_user_from_db), db: Session = Depends(get_db)):
    db_maparam = db.query(MaparamMemberModel).filter(MaparamMemberModel.user_id == user.id).all()
    maparam_list = []
    for i in db_maparam:
        maparam_list.append(i.maparam)
    if db_maparam is None:
        raise HTTPException(status_code=404, detail="maparam not found")
    return maparam_list


@router.get("/search/{word}")
def search_maparam(word: str, db: Session = Depends(get_db)):
    return db.query(MaparamModel).filter(MaparamModel.name.like("%" + word + "%")).all()
