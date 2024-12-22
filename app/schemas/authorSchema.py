from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuthorBase(BaseModel):
  name: str
  birthDate: Optional[datetime] = None

  class Config:
    orm_mode = True