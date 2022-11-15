from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
import re

from db.database import get_db
from schemas.user import UserBase, UserDisplay
from repositories.user import UserRepository


router = APIRouter(
  tags=['/user'],
  prefix='/user'
)

@router.post("/", response_model = UserDisplay, status_code=201)
def create(request: UserBase, db: Session = Depends(get_db)):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if not re.fullmatch(regex, request.email):
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = 'Invalid email format'
        ) 
    try:
        new_user = UserRepository.create_user(db, request)
    except:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT, detail='email already exists'
        )
    return new_user
  
# @router.get("/", response_model = List[UserDisplay])
# def create(db: Session = Depends(get_db)):
#     return db.query(User).all()
