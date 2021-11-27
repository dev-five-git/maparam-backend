from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    pw: str
    email: str
    age: int
    hashtag: str

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    name: Optional[str]
    pw: Optional[str]
    email: Optional[str]
    age: Optional[int]
    hashtag: Optional[str]

    class Config:
        orm_mode = True


class UserId(BaseModel):
    id: str


class UserPw(BaseModel):
    pw: str



