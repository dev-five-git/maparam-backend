from typing import Optional

from pydantic import BaseModel


class TodayBoardComment(BaseModel):
    board_index: int
    writer: str
    content: str

    class Config:
        orm_mode = True


class UpdateTodayBoardComment(BaseModel):
    content: Optional[str]

    class Config:
        orm_mode = True
