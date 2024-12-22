from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
  title: str
  publishedYear: Optional[int] = None
  author_id: int
  user_id: Optional[int] = None

  class Config:
    orm_mode = True