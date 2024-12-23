from app.schemas.author_schema import AuthorBase
from .generic_response import GenericResponse
from typing import Optional

class AuthorResponse(GenericResponse):
  author: Optional[AuthorBase] = None
