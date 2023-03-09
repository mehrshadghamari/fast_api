from pydantic import BaseModel
from typing import Optional,List



class Blog(BaseModel):
    title:str
    body:str
    # page:int
    # published:Optional[str]



class User(BaseModel):

    name:str
    email:str
    password:str



class ShowUser(BaseModel):
    name:str
    email:str
    blogs: List[Blog] 
    # password:str

    class Config():
        orm_mode=True


class ShowBlog(BaseModel):
    title:str
    body:str
    creator:Optional[ShowUser]
    class Config:
        orm_mode=True