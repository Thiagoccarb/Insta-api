from sqlalchemy.orm import Session

from db.models import User
from schemas.user import UserBase
from hash.hash import Hash

class UserRepository():
    @staticmethod
    def create_user(db: Session, request: UserBase) -> User:
        new_user = User(     
            name = request.name,
            email = request.email,
            username = request.username,
            password = Hash.bcrypt(request.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def existing_user_by_id(db: Session, id: int):
        user = db.query(User).filter(User.id == id).first()
        return user is not None
    
    @staticmethod
    def get_user_by_id(db: Session, id: int):
        user = db.query(User).filter(User.id == id).first()
        return user