from sqlalchemy.orm import Session
from app.models.user import User
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.dto import *
from app.schemas.user_schema import UserBase
from app.config import SECRET_KEY, TOKEN_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .base_controller import BaseController
from fastapi import Depends, HTTPException, status
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
logger = logging.getLogger("TokenController")
class TokenController(BaseController):
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def verify_password(self, plain_password: str, hashed_password: str) -> bool:
    #Verify the hashed password.
    return TokenController.pwd_context.verify(plain_password, hashed_password)

  def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
    #Create a JWT token.
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt

  def verify_token(self, token: str) -> Optional[dict]:
    #Verify and decode the JWT token.
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
      return payload
    except JWTError:
      return None

  def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
          raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = db.query(User).filter(User.email == email).first()
    if db_user is None:
        raise credentials_exception
    return db_user
  
  def authenticate_user(self, email: str, password: str):
    # Authenticate user by email and password.
    db_user = self.db.query(User).filter(User.email == email).first()
    if not db_user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
      )
    if not self.verify_password(password, db_user.hashed_password):
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
      )
    return db_user

  def login_user(self, user: UserCredentialsRequest):
    # Login user and return JWT token.
    user = self.authenticate_user(user.email, user.password)
    access_token = self.create_access_token(
      data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    user_base = UserBase.from_orm(user)
    return LoginResponse(
      success = True,
      access_token = access_token,
      token_type = "bearer",
      user = user_base
    )