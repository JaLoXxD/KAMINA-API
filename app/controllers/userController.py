from sqlalchemy.orm import Session
from app.models.user import User
from datetime import datetime, timedelta
from app.schemas.userSchema import UserBase
from app.dto.request.userCreate import UserCreate
from app.dto.request.userCredentials import UserCredentials
from app.dto.response.userCreateResponse import UserCreateResponse
from .baseController import BaseController
from app.exceptions import ExceptionHandlers
from .tokenController import TokenController
import logging


logger = logging.getLogger("UserController")
class UserController(BaseController):

  @staticmethod
  def createUser(user: UserCreate, db: Session):
    try:
      hashedPassword = TokenController.hash_password(user.password)
      db_user = User(
        name=user.name,
        email=user.email,
        hashedPassword=hashedPassword,
        registerDate=datetime.now()
      )
      db.add(db_user)
      db.commit()
      db.refresh(db_user)
      user_base = UserBase.from_orm(db_user)
      response = UserCreateResponse(success=True, message="User created successfully", userCreated=user_base)
      logger.info(f"User created with ID: {db_user.id}")
      return response
    except Exception as e:
      logger.error(f"Error creating user: {e}")
      db.rollback()
      # return await ExceptionHandlers.global_exception_handler(None, e) 
      return UserController.manageError(e)

  @staticmethod
  def authenticateUser(email: str, password: str, db: Session):
    #Authenticate user by email and password.
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
      )
    if not TokenController.verify_password(password, db_user.hashedPassword):
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
      )
    return db_user

  @staticmethod
  def loginUser(user: UserCredentials, db: Session):
    #Login user and return JWT token.
    user = UserController.authenticateUser(user.email, user.password, db)
    access_token = TokenController.create_access_token(
      data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {
      "success": True,
      "access_token": access_token,
      "token_type": "bearer",
      "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email
      }
    }
