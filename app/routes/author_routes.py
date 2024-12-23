from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dto import *
from app.controllers.author_controller import AuthorController
from app.controllers.token_controller import TokenController
import logging

router = APIRouter(prefix="/authors")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("authorsApi")

@router.post("/", response_model = AuthorResponse)
def create_author(author: AuthorRequest, controller: AuthorController = Depends(AuthorController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.create_author(author)

@router.get("/{id}", response_model = AuthorResponse)
def get_author_by_id(id: int, controller: AuthorController = Depends(AuthorController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.get_author_by_id(id)

@router.put("/{id}")
def update_author(id: int, author: AuthorRequest, controller: AuthorController = Depends(AuthorController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.update_author(id, author)

@router.delete("/{id}")
def delete_author(id: int, controller: AuthorController = Depends(AuthorController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.delete_author(id)