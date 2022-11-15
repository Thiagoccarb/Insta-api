from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from .user import User
from Enums.picture_url import PictureUrl
    
class PostBase(BaseModel): 
    image_url: str
    image_url_type: PictureUrl
    caption: str
    
    class Config():
        orm_mode = True
        
class Comment(BaseModel): 
    text: str
    username: str
    timestamp: datetime
    
    class Config():
        orm_mode = True
        
class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timeStamp: datetime
    user: User
    comments: List[Comment]
    
    class Config():
        orm_mode = True
        
class UpdatePost(BaseModel):
    image_url: Optional[str]
    image_url_type: Optional[PictureUrl]
    caption: Optional[str]
    
    class Config():
        orm_mode = True
