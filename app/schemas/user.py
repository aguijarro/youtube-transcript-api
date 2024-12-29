from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserBase):
    password: Optional[str] = None
    
class UserInDB(UserBase):
    id: int
    
    class Config:
        from_attributes = True
        
class User(UserInDB):
    pass 