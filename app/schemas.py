from pydantic import BaseModel, EmailStr
from typing import Optional



class UserEntry(BaseModel):
    email: EmailStr
    password: str
    name: str
    username: str
    age: Optional[int] = None
    raca: Optional[str] = None
    uf: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    age: Optional[int] = None
    raca: Optional[str] = None
    uf: Optional[str] = None
    is_active: Optional[bool] = True


class Token(BaseModel):
	access_token: str
	token_type: str
