from pydantic import BaseModel
from typing import Optional

class RentBookRequest(BaseModel):
  user_id: int
  book_id: int