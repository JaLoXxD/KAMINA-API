from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import SECRET_KEY, TOKEN_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .baseController import BaseController

import logging

logger = logging.getLogger("TokenController")
class TokenController(BaseController):
  # Password hashing utility
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

  def hash_password(password: str) -> str:
    #Hash the user's password.
    return TokenController.pwd_context.hash(password)

  def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Verify the hashed password.
    return TokenController.pwd_context.verify(plain_password, hashed_password)

  def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    #Create a JWT token.
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt

  def verify_token(token: str) -> Optional[dict]:
    #Verify and decode the JWT token.
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
      return payload
    except JWTError:
      return None