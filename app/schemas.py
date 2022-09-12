from datetime import datetime
import typing

import pydantic
from . import utils

class UserCreate(pydantic.BaseModel):
    name: str
    email: pydantic.EmailStr
    password: str



class UserShow(pydantic.BaseModel):
    id: int
    name: str
    email: pydantic.EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str



class PostBase(pydantic.BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    ...


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserShow

    class Config:
        orm_mode = True


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str



class TokenData(pydantic.BaseModel):
    idx: typing.Optional[str] = None


