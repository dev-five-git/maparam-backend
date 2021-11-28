from typing import Optional

from pydantic import BaseModel


class Maparam(BaseModel):
    creater_id: str
    name: str
    max_member_size: int
    introduce: str

    class Config:
        orm_mode = True


class UpdateMaparam(BaseModel):
    name: Optional[str]
    max_member_size: Optional[int]
    introduce: Optional[str]

    class Config:
        orm_mode = True
