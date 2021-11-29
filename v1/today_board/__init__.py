from typing import Optional

from pydantic import BaseModel


class TodayBoard(BaseModel):
    keyword: str
    content: str

    class Config:
        orm_mode = True


class UpdateTodayBoard(BaseModel):
    content: Optional[str]
    image: Optional[str]

    class Config:
        orm_mode = True
