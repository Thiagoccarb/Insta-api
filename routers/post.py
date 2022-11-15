from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import random
import string 
import shutil

from db.database import get_db
from schemas.post import PostBase, PostDisplay, UpdatePost
from repositories.post import PostRepository
from repositories.user import UserRepository
from authentication.auth import UserAuth
from authentication.oauth2 import get_current_user


router = APIRouter(
  tags=['/post'],
  prefix='/post'
)

@router.post("/", response_model = PostDisplay, status_code=201)
def create(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    id = int(current_user.id)
    existing_user = UserRepository.existing_user_by_id(db, id)
    if not existing_user:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = 'User not found'
    ) 
    new_post = PostRepository.create_post(db, request, id)
    return new_post
  
@router.get("/all", response_model = List[PostDisplay], status_code=200)
def get_all (db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    id = int(current_user.id)
    return PostRepository.get_all_posts(db, id)
  
@router.get("/{id}", response_model = PostDisplay, status_code=200)
def get_by_id (id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user),):
    user_id = int(current_user.id)
    post = PostRepository.get_post_by_id(db, user_id, id)
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Post not found'
        ) 
    return post

@router.delete("/{id}", status_code=204)
def remove_by_id (id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user),):
    user_id = int(current_user.id)
    PostRepository.delete_post_by_id(db, user_id, id)
  
@router.patch("/{id}", response_model=PostDisplay)
def update_by_id (id: int, request: UpdatePost, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user),):
    user_id = int(current_user.id)
    updated_post = PostRepository.update_post_by_id(db, user_id, id, request)
    if not updated_post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Post not found'
        ) 
    return updated_post
    
@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    alphabet = string.ascii_letters
    rand_str = ''.join(random.choice(alphabet) for i in range(5))
    formated_rand_str = f'_{rand_str}.'
    filename = formated_rand_str.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}
    
  