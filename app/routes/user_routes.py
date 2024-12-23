from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.dto import *
from app.controllers.user_controller import UserController
from app.controllers.token_controller import TokenController
import logging

router = APIRouter(prefix="/users")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("userApi")

@router.get("/raise-unexpected-exception")
async def raise_unexpected_exception():
  raise Exception("Unexpected error occurred")

@router.post("/register", response_model=UserResponse)
def create_user(user: UserRequest, controller: UserController = Depends(UserController)):
  return controller.create_user(user)

@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, controller: UserController = Depends(UserController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.get_user_by_id(id)

@router.put("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, user: UserRequest, controller: UserController = Depends(UserController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.update_user_by_id(id, user)

@router.delete("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, controller: UserController = Depends(UserController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.delete_user_by_id(id)

@router.post("/login")
def login_user(user: UserCredentialsRequest, controller: TokenController = Depends(TokenController)):
  return controller.login_user(user)
