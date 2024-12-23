from app.models.author import Author
from app.schemas.author_schema import AuthorBase
from sqlalchemy.orm import Session
from .base_controller import BaseController
from app.dto import *
from datetime import datetime
from fastapi import Depends
from app.database import get_db
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("AuthorController")

class AuthorController(BaseController):

  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def create_author(self, author: AuthorRequest):
    birth_date = datetime.strptime(author.birth_date, "%d/%m/%Y") if author.birth_date else None
    db_author = Author(name=author.name, birth_date=birth_date)
    self.db.add(db_author)
    self.db.commit()
    self.db.refresh(db_author)
    author_base = AuthorBase.from_orm(db_author)
    response = AuthorResponse(success=True, message="Author created successfully", author=author_base)
    logger.info(f"Author created with ID: {db_author.id}")
    return response

  def get_author_by_id(self, id: int):
    try:
      author = self.db.query(Author).filter(Author.id == id).first()
      if not author:
        return AuthorResponse(success=False, message="Author not found")
      author_base = AuthorBase.from_orm(author)
      return AuthorResponse(success=True, message="Author retrieved successfully", author=author_base)
    except Exception as e:
      logger.error(f"Error retrieving author: {e}")
      return self.manage_error(e)

  def update_author(self, id: int, author_update: AuthorRequest):
    try:
      db_author = self.db.query(Author).filter(Author.id == id).first()
      if not db_author:
        return AuthorResponse(success=False, message="Author not found")
      
      db_author.name = author_update.name
      db_author.birth_date = datetime.strptime(author_update.birth_date, "%d/%m/%Y") if author_update.birth_date else None
      
      self.db.commit()
      self.db.refresh(db_author)
      author_base = AuthorBase.from_orm(db_author)
      return AuthorResponse(success=True, message="Author updated successfully", author=author_base)
    except Exception as e:
      logger.error(f"Error updating author: {e}")
      self.db.rollback()
      return self.manage_error(e)

  def delete_author(self, id: int):
    try:
      author = self.db.query(Author).filter(Author.id == id).first()
      if not author:
        error_response = AuthorResponse(success=False, message="Author not found")
        return JSONResponse(status_code=400, content=error_response.dict())
      self.db.delete(author)
      self.db.commit()
      return AuthorResponse(success=True, message="Author deleted successfully")
    except Exception as e:
      logger.error(f"Error deleting author: {e}")
      self.db.rollback()
      return self.manage_error(e)