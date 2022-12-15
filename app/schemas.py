import typing
from datetime import datetime

import pydantic


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


class PostVote(pydantic.BaseModel):
    Posts: Post
    votes: int

    class Config:
        orm_mode = True


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    idx: typing.Optional[str] = None


class Vote(pydantic.BaseModel):
    post_id: int
    direction: int

    @pydantic.validator('direction')
    def direction_must_be_1_or_zero(cls, v):
        if v not in (1, 0):
            raise ValueError('direction must be 1 or 0')
        return v
