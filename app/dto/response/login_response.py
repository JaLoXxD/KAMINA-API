from pydantic import BaseModel
from app.schemas.user_schema import UserBase
from typing import Optional

class LoginResponse(BaseModel):
  success: bool
  access_token: str
  token_type: str
  user: Optional[UserBase]