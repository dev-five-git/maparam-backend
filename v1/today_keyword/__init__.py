import datetime

from pydantic import BaseModel


class Keyword(BaseModel):
    keyword: str
    date: datetime.date

    class Config:
        orm_mode = True
