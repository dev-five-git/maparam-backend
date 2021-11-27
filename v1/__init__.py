from fastapi import APIRouter

from .today_board.today_board import router as today_router
from .today_keyword.today_keyword import router as keyword_router
from .user.user import router as user_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["user"])
v1_router.include_router(keyword_router, prefix="/todaykeyword", tags=["today keyword"])
v1_router.include_router(today_router, prefix="/todayboard", tags=["today board"])
