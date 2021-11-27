from typing import Optional

from pydantic import BaseModel


class TodayBoard(BaseModel):
    keyword: str
    writer: str
    content: str
    image: str

    class Config:
        orm_mode = True


class UpdateTodayBoard(BaseModel):
    keyword: Optional[str]
    writer: Optional[str]
    content: Optional[str]
    image: Optional[str]

    class Config:
        orm_mode = True
