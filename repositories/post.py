from sqlalchemy.orm import Session
from db.models import Post
from schemas.post import PostBase, UpdatePost
from datetime import datetime


class PostRepository():
    @staticmethod
    def create_post(db: Session, request: PostBase, id: int):
        new_post = Post(
            image_url= request.image_url,
            image_url_type = request.image_url_type,
            caption = request.caption,
            timeStamp = datetime.now(),
            user_id = id,
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    
    @staticmethod
    def get_all_posts(db: Session, id: int):
        return db.query(Post).filter(Post.user_id == id).all()
    
    @staticmethod
    def get_post_by_id(db: Session, user_id: int, post_id: int):
        post = db.query(Post).filter(
            Post.user_id == user_id, 
            Post.id == post_id
        ).first()
        if not post:
            return None
        return post
        
    @staticmethod
    def delete_post_by_id(db: Session, user_id: int, post_id: int):
        post = db.query(Post).filter(
            Post.user_id == user_id, 
            Post.id == post_id
        ).first()
        if post:
            db.delete(post)
            db.commit()
            
    @staticmethod
    def update_post_by_id(db: Session, user_id: int, post_id: int, request: UpdatePost):
        post = db.query(Post).filter(
            Post.user_id == user_id, 
            Post.id == post_id
        ).first()
        if not post:
            return None
        post_data = {
            **request.dict(exclude_unset=True),
            'timeStamp': datetime.now()
        } 
        for key, value in post_data.items():
            setattr(post, key, value)
        db.commit()
        return post
        
