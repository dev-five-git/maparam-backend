from typing import Optional

from pydantic import BaseModel


class MaparamNotice(BaseModel):
    maparam_index: int
    writer: str
    content: str
    image: str

    class Config:
        orm_mode = True


class UpdateMaparamNotice(BaseModel):
    content: Optional[str]
    image: Optional[str]

    class Config:
        orm_mode = True
