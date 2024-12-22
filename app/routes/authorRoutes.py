from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dto import *
from app.controllers.authorController import AuthorController
import logging

router = APIRouter(prefix="/authors")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("authorsApi")

@router.post("/create", response_model=UserCreateResponse)
def createUser(user: UserCreate, db: Session = Depends(get_db)):
  return UserController.createUser(user, db)

@router.post("/login")
def loginUser(user: UserCredentials, db: Session = Depends(get_db)):
  return UserController.loginUser(user, db)
