from pydantic import BaseModel

class UserBase(BaseModel): 
    name: str
    email: str
    username: str
    password: str
    
class User(BaseModel):
    username: str
    
    class Config():
        orm_mode = True
    
class UserDisplay(BaseModel): 
    id = int
    name: str
    email: str
    username: str

    class Config():
        orm_mode = True