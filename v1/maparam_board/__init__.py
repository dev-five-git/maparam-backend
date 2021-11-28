from typing import Optional

from pydantic import BaseModel


class MaparamBoard(BaseModel):
    maparam_index: int
    writer: str
    content: str
    image: str

    class Config:
        orm_mode = True


class UpdateMaparamBoard(BaseModel):
    writer: Optional[str]
    content: Optional[str]
    image: Optional[str]

    class Config:
        orm_mode = True
