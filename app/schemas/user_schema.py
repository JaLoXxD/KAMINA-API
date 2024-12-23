from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
  id: int
  name: str
  email: str
  register_date: datetime

  class Config:
    orm_mode = True
    from_attributes = True