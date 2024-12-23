from sqlalchemy.orm import Session
from app.models.user import User
from datetime import datetime, timedelta
from app.schemas.user_schema import UserBase
from app.dto import *
from app.exceptions import ExceptionHandlers
from .base_controller import BaseController
from app.database import get_db
from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.utils.security import hash_password
from app.utils.commons import is_valid_mail
import logging

logger = logging.getLogger("UserController")

class UserController(BaseController):

  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def create_user(self, user: UserRequest):
    try:
      if not is_valid_mail(user.email):
        error_response = UserResponse(success=False, message="Invalid email")
        return JSONResponse(status_code=400, content=error_response.dict())
      hashed_password = hash_password(user.password)
      db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        register_date=datetime.now()
      )
      self.db.add(db_user)
      self.db.commit()
      self.db.refresh(db_user)
      user_base = UserBase.from_orm(db_user)
      response = UserResponse(success=True, message="User created successfully", user=user_base)
      logger.info(f"User created with ID: {db_user.id}")
      return response
    except Exception as e:
      logger.error(f"Error creating user: {e}")
      self.db.rollback()
      return self.manage_error(e)

  def get_user_by_id(self, user_id: int):
    try:
      user = self.db.query(User).filter(User.id == user_id).first()
      if not user:
        return UserResponse(success=False, message="User not found")
      user_base = UserBase.from_orm(user)
      return UserResponse(success=True, message="User retrieved successfully", user=user_base)
    except Exception as e:
      logger.error(f"Error retrieving user: {e}")
      return self.manage_error(e)

  def update_user_by_id(self, user_id: int, user_update: UserRequest):
    try:
      user = self.db.query(User).filter(User.id == user_id).first()
      if not user:
        return UserResponse(success=False, message="User not found")
      user.name = user_update.name
      user.email = user_update.email
      if user_update.password:
        user.hashed_password = hash_password(user_update.password)
      self.db.commit()
      self.db.refresh(user)
      user_base = UserBase.from_orm(user)
      return UserResponse(success=True, message="User updated successfully", user=user_base)
    except Exception as e:
      logger.error(f"Error updating user: {e}")
      self.db.rollback()
      return self.manage_error(e)

  def delete_user_by_id(self, user_id: int):
    try:
      user = self.db.query(User).filter(User.id == user_id).first()
      if not user:
        return GenericResponse(success=False, message="User not found")
      self.db.delete(user)
      self.db.commit()
      return GenericResponse(success=True, message="User deleted successfully")
    except Exception as e:
      logger.error(f"Error deleting user: {e}")
      self.db.rollback()
      return self.manage_error(e)

  def user_exists(self, email: str = None, user_id: int = None):
    try:
      if email:
        user = self.db.query(User).filter(User.email == email).first()
        if user:
          return True
      if user_id:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
          return True
      return False
    except Exception as e:
      logger.error(f"Error checking if user exists: {e}")
      return False
