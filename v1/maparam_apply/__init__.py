from pydantic import BaseModel


class MaparamApply(BaseModel):
    user_id: str
    maparam_index: int

    class Config:
        orm_mode = True


class ApplyCheck(BaseModel):
    status: int

    class Config:
        orm_mode = True
