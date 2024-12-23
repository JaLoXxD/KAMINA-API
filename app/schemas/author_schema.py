from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class AuthorBase(BaseModel):
  id: int
  name: str
  birth_date: Optional[str] = None

  class Config:
    orm_mode = True
    from_attributes = True

  # Validator to format `birth_date`
  @validator("birth_date", pre=True, always=True)
  def format_birth_date(cls, value: Optional[datetime]) -> Optional[str]:
    if value:
      return value.strftime("%d/%m/%Y")  # Convert datetime to string
    return None