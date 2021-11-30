# Community Comment
import copy

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.MaparamBoardComment import MaparamBoardCommentModel
from ..models.MaparamBoard import MaparamBoardModel
from ..models.user import UserModel
from ..notification.notification import create_noti

router = APIRouter()


@router.post("/")
def create_board_comment(community_comment: MaparamBoardComment, db: Session = Depends(get_db)):
    db_community_comment = MaparamBoardCommentModel(board_index=community_comment.board_index,
                                                    writer=community_comment.writer,
                                                    content=community_comment.content)
    # 알림 생성
    db_board = db.query(MaparamBoardModel).filter(
        MaparamBoardModel.index == community_comment.board_index).one_or_none()
    comment_writer_name = db.query(UserModel).filter(UserModel.id == community_comment.writer).one_or_none().name
    if db_board.writer != community_comment.writer:
        create_noti(db, db_board.writer, "마파람 \"" + db_board.maparam.name + "\"", comment_writer_name)

    db.add(db_community_comment)
    db.commit()
    db.refresh(db_community_comment)
    return db_community_comment


# @router.get("/{index}")
# def get_community_board_by_index(index: int, db: Session = Depends(get_db)):
#     db_community_comment = db.query(MaparamBoardCommentModel).filter(MaparamBoardCommentModel.index == index).one_or_none()
#     if db_community_comment is None:
#         raise HTTPException(status_code=404, detail="Comment not found")
#     return db_community_comment


@router.put("/{index}")
def update_board_comment(index: int, community_comment: UpdateMaparamBoardComment, db: Session = Depends(get_db)):
    db_community_comment = db.query(MaparamBoardCommentModel).filter(MaparamBoardCommentModel.index == index).one_or_none()
    if db_community_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    for var, value in vars(community_comment).items():
        setattr(db_community_comment, var, value) if value else None

    db.add(db_community_comment)
    db.commit()
    db.refresh(db_community_comment)
    return db_community_comment


@router.delete("/{index}")
def delete_board_comment(index: int, db: Session = Depends(get_db)):
    db_community_comment = db.query(MaparamBoardCommentModel).filter(MaparamBoardCommentModel.index == index).one_or_none()
    if db_community_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    a = copy.deepcopy(db_community_comment.__dict__)
    db.delete(db_community_comment)
    db.commit()
    return a


#
@router.get("/{index}/comment")
def get_comment_by_board_index(index: int, db: Session = Depends(get_db)):
    db_community = db.query(MaparamBoardModel).filter(MaparamBoardModel.index == index).one_or_none()
    if db_community is None:
        raise HTTPException(status_code=404, detail="comment not found")
    return db_community.maparam_board_comment
