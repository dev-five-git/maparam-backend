from fastapi import APIRouter

from .user.user import router as user_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["user"])
