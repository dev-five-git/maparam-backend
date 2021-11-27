from fastapi import APIRouter

from .maparam.maparam import router as maparam_router
from .maparam_apply.maparam_apply import router as maparam_apply_router
from .maparam_member.maparam_member import router as maparam_member_router
from .timeline_board.timeline_board import router as timeline_router
from .timeline_comment.timeline_comment import router as timeline_comment_router
from .today_board.today_board import router as today_router
from .today_comment.today_comment import router as today_comment_router
from .today_keyword.today_keyword import router as keyword_router
from .user.user import router as user_router

v1_router = APIRouter()

v1_router.include_router(user_router, prefix="/user", tags=["user"])
v1_router.include_router(keyword_router, prefix="/todaykeyword", tags=["today keyword"])
v1_router.include_router(today_router, prefix="/todayboard", tags=["today board"])
v1_router.include_router(today_comment_router, prefix="/today/comment", tags=["today board-comment"])
v1_router.include_router(timeline_router, prefix="/timeline", tags=["timeline board"])
v1_router.include_router(timeline_comment_router, prefix="/timeline/comment", tags=["timeline board-comment"])
v1_router.include_router(maparam_router, prefix="/maparam", tags=["maparam"])
v1_router.include_router(maparam_member_router, prefix="/maparam/member", tags=["maparam member"])
v1_router.include_router(maparam_apply_router, prefix="/maparam/apply", tags=["maparam apply"])
