# Community Comment
import copy

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import *
from ..models import get_db
from ..models.TodayBoard import TodayBoardModel
from ..models.TodayComment import TodayCommentModel

router = APIRouter()


@router.post("/")
def create_board_comment(community_comment: TodayBoardComment, db: Session = Depends(get_db)):
    db_community_comment = TodayCommentModel(board_index=community_comment.board_index,
                                             writer=community_comment.writer,
                                             content=community_comment.content)
    db.add(db_community_comment)
    db.commit()
    db.refresh(db_community_comment)
    return db_community_comment


@router.get("/{index}")
def get_community_board_by_index(index: int, db: Session = Depends(get_db)):
    db_community_comment = db.query(TodayCommentModel).filter(TodayCommentModel.index == index).one_or_none()
    if db_community_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_community_comment


@router.put("/{index}")
def update_board_comment(index: int, community_comment: UpdateTodayBoardComment, db: Session = Depends(get_db)):
    db_community_comment = db.query(TodayCommentModel).filter(TodayCommentModel.index == index).one_or_none()
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
    db_community_comment = db.query(TodayCommentModel).filter(TodayCommentModel.index == index).one_or_none()
    if db_community_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    a = copy.deepcopy(db_community_comment.__dict__)
    db.delete(db_community_comment)
    db.commit()
    return a


#
@router.get("/{index}/comment")
def get_comment_by_board_index(index: int, db: Session = Depends(get_db)):
    db_community = db.query(TodayBoardModel).filter(TodayBoardModel.index == index).one_or_none()
    if db_community is None:
        raise HTTPException(status_code=404, detail="comment not found")
    return db_community.community_comment
