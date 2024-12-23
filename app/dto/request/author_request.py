from pydantic import BaseModel
from typing import Optional

class AuthorRequest(BaseModel):
  name: str
  birth_date: Optional[str] = None