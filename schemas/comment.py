from pydantic import BaseModel


class CommentBase(BaseModel): 
    text: str
    username: str
    post_id: int