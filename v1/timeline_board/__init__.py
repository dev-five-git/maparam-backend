from typing import Optional

from pydantic import BaseModel


class TimelineBoard(BaseModel):
    location_latitude: float
    location_longitude: float
    writer: str
    content: str
    image: str
    hashtag: str

    class Config:
        orm_mode = True


class UpdateTimelineBoard(BaseModel):
    writer: Optional[str]
    content: Optional[str]
    image: Optional[str]
    hashtag: Optional[str]

    class Config:
        orm_mode = True


class CurrentLocation(BaseModel):
    location_latitude: float
    location_longitude: float
