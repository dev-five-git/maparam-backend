from typing import Optional

from pydantic import BaseModel


class MaparamMember(BaseModel):
    user_id: str
    maparam_index: int

    class Config:
        orm_mode = True


class UpdateMaparamMember(BaseModel):
    tier: Optional[int]

    class Config:
        orm_mode = True
