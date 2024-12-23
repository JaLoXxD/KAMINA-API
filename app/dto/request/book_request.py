from pydantic import BaseModel
from typing import Optional

class BookRequest(BaseModel):
  title: str
  published_year: Optional[int] = None
  author_id: int
  user_id: Optional[int] = None