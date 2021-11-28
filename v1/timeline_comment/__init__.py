from typing import Optional

from pydantic import BaseModel


class TimelineBoardComment(BaseModel):
    board_index: int
    writer: str
    content: str

    class Config:
        orm_mode = True


class UpdateTimelineBoardComment(BaseModel):
    content: Optional[str]

    class Config:
        orm_mode = True
