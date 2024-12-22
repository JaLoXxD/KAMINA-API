from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
  name: str
  email: str
  registerDate: datetime

  class Config:
    orm_mode = True
    from_attributes = True