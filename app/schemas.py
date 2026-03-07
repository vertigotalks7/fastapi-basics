from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

class PostCreate(PostBase):  # inherits from PostBase
  pass

class Post(PostBase):
  id: int
  created_at: datetime
  owner_id: int
  owner: Userout

  class Config:
    from_attributes = True

class PostOut(BaseModel):
  Post: Post
  votes: int

  class Config:
    from_attributes = True

class UserCreate(BaseModel):
  email: EmailStr
  password: str

class Userout(BaseModel):
  email: EmailStr
  id: int
  created_at: datetime

  class Config:
    from_attributes = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[int] = None

class Vote(BaseModel):
  post_id: int
  dir: conint(le=1) # direction of vote (upvote or downvote)