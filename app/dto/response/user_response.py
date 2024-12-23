from app.schemas.user_schema import UserBase
from .generic_response import GenericResponse
from typing import Optional

class UserResponse(GenericResponse):
  user: Optional[UserBase] = None
