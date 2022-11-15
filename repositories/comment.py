from sqlalchemy.orm import Session
from datetime import datetime

from db.models import Comment
from schemas.comment import CommentBase

class CommentRepository():
    @staticmethod
    def create_comment(db: Session, request: CommentBase):
        new_comment = Comment(     
            text = request.text,
            username = request.username,
            post_id = request.post_id,
            timestamp = datetime.now()
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    
    @staticmethod
    def get_all_comments_by_id(db: Session, post_id: int):
        comments = db.query(Comment).filter(Comment.id == post_id).all()
        return comments