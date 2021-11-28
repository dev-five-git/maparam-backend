from typing import Optional

from pydantic import BaseModel


class MaparamBoard(BaseModel):
    maparam_name: str
    writer: str
    content: str
    image: str

    class Config:
        orm_mode = True


class UpdateMaparamBoard(BaseModel):
    maparam_name: Optional[str]
    writer: Optional[str]
    content: Optional[str]
    image: Optional[str]

    class Config:
        orm_mode = True
