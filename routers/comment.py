from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session


from db.database import get_db
from schemas.comment import CommentBase
from repositories.comment import CommentRepository
from authentication.auth import UserAuth
from authentication.oauth2 import get_current_user


router = APIRouter(
  tags=['/comment'],
  prefix='/comment'
)

@router.post("/", status_code=201)
def create(request: CommentBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    new_comment = CommentRepository.create_comment(db, request)
    return new_comment
  
@router.get("/all/{post_id}")
def get_all (post_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return CommentRepository.get_all_comments_by_id(db, post_id)
    
  