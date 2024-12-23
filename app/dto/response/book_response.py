from app.schemas.book_schema import BookBase
from .generic_response import GenericResponse
from typing import Optional, List

class BookResponse(GenericResponse):
  book: Optional[BookBase] = None
