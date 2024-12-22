from app.schemas.userSchema import UserBase
from .genericResponse import GenericResponse

class UserCreateResponse(GenericResponse):
  userCreated: UserBase
