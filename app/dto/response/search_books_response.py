from app.schemas.book_schema import BookBase
from .generic_response import GenericResponse
from typing import Optional, List

class SearchBooksResponse(GenericResponse):
  books: Optional[List[BookBase]] = None
