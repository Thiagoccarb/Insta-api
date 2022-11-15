from .database import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(30))
    email = Column(String(30), unique = True)
    username = Column(String(30))
    password = Column(String(30))
    posts = relationship('Post', back_populates='user')
    
class Post(Base):
    __tablename__="post"
    id = Column(Integer, primary_key = True, index = True)
    image_url =Column(String)
    image_url_type =Column(String)
    caption =Column(String)
    timeStamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    
class Comment(Base):
    __tablename__="comment"
    id = Column(Integer, primary_key = True, index = True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='comments')