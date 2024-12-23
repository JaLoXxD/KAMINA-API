from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .author_schema import AuthorBase
from .user_schema import UserBase

class BookBase(BaseModel):
  id: int
  title: str
  published_year: Optional[int] = None
  user: Optional[UserBase] = None
  author: Optional[AuthorBase] = None

  class Config:
    orm_mode = True
    from_attributes = True