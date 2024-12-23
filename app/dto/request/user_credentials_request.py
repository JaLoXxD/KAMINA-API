from pydantic import BaseModel

class UserCredentialsRequest(BaseModel):
  email: str
  password: str