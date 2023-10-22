from pydantic import BaseModel, EmailStr
from typing import Optional



class UserEntry(BaseModel):
    email: EmailStr
    password: str
    name: str
    username: str
    age: Optional[int] = None
    raca: Optional[str] = None
    genero: Optional[str] = None
    uf: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    age: Optional[int] = None
    raca: Optional[str] = None
    genero: Optional[str] = None
    uf: Optional[str] = None
    is_active: Optional[bool] = True


class PostEntry(BaseModel):
    title: str
    body: str

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class ReplyEntry(BaseModel):
    body: str

class ReplyUpdate(BaseModel):
    body: Optional[str] = None


class Token(BaseModel):
	access_token: str
	token_type: str
