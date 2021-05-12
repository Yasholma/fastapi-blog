from pydantic import BaseModel
from typing import Any


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):
    message: str
    data: Any

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True
