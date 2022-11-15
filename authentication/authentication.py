from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from hash.hash import Hash
from db.database import get_db
from db.models import User
from schemas.user import UserDisplay
from authentication.oauth2 import create_access_token

router = APIRouter(
  tags=['authentication']
)

@router.post('/auth')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    unauthorized_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not user:
        raise unauthorized_exception
    print(Hash.verify(user.password, request.password))
    if not Hash.verify(user.password, request.password):
         raise unauthorized_exception
    access_token = create_access_token({'id': user.id})
    return {
      'access_token': access_token,
      'token_type': 'bearer'
    }