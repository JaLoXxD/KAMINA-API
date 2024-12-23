from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .base_controller import BaseController
from app.models.author import Author
from app.models.book import Book
from app.dto import *
from app.schemas.book_schema import BookBase
from app.controllers.user_controller import UserController
from app.database import get_db
from fastapi import Depends
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("BookController")

class BookController(BaseController):

  def __init__(self, db: Session = Depends(get_db), user_controller: UserController = Depends(UserController)):
    self.db = db
    self.user_controller = user_controller

  def create_book(self, book: BookRequest):
    try:
      db_book = Book(
        title=book.title,
        published_year=book.published_year,
        author_id=book.author_id,
      )
      self.db.add(db_book)
      self.db.commit()
      self.db.refresh(db_book)
      book_base = BookBase.from_orm(db_book)
      response = BookResponse(success=True, message="Book created successfully", book=book_base)
      logger.info(f"Book created with ID: {db_book.id}")
      return response
    except IntegrityError as e:
      logger.error(f"Integrity error creating book: {e}")
      self.db.rollback()
      error_response = BookResponse(success=False, message="Failed to create book due to foreign key constraint. Please ensure the author exists.")
      return JSONResponse(status_code=400, content=error_response.dict())
    except Exception as e:
      logger.error(f"Error creating book: {e}")
      self.db.rollback()
      return self.manage_error(e)

  def get_book_by_id(self, book_id: int):
    try:
      book = self.db.query(Book).filter(Book.id == book_id).first()
      if not book:
        return BookResponse(success=False, message="Book not found")
      book_base = BookBase.from_orm(book)
      return BookResponse(success=True, message="Book retrieved successfully", book=book_base)
    except Exception as e:
      logger.error(f"Error retrieving book: {e}")
      return self.manage_error(e)

  def update_book_by_id(self, book_id: int, book_update: BookRequest):
    try:
      book = self.db.query(Book).filter(Book.id == book_id).first()
      if not book:
        return BookResponse(success=False, message="Book not found")
      book.title = book_update.title
      book.published_year = book_update.published_year
      book.author_id = book_update.author_id
      self.db.commit()
      self.db.refresh(book)
      book_base = BookBase.from_orm(book)
      return BookResponse(success=True, message="Book updated successfully", book=book_base)
    except IntegrityError as e:
      logger.error(f"Integrity error updating book: {e}")
      self.db.rollback()
      error_response = BookResponse(success=False, message="Failed to update book due to foreign key constraint.")
      return JSONResponse(status_code=400, content=error_response.dict())
    except Exception as e:
      logger.error(f"Error updating book: {e}")
      self.db.rollback()
      return self.manage_error(e)

  def delete_book_by_id(self, book_id: int):
    try:
      book = self.db.query(Book).filter(Book.id == book_id).first()
      if not book:
        return GenericResponse(success=False, message="Book not found")
      self.db.delete(book)
      self.db.commit()
      return GenericResponse(success=True, message="Book deleted successfully")
    except Exception as e:
      logger.error(f"Error deleting book: {e}")
      self.db.rollback()
      return self.manage_error(e)

  def search_books(self, title: str = None, author_name: str = None, published_year: int = None):
    try:
      query = self.db.query(Book)
      if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
      if author_name:
        query = query.join(Author).filter(Author.name.ilike(f"%{author_name}%"))
      if published_year:
        query = query.filter(Book.published_year == published_year)
      books = query.all()
      book_bases = [BookBase.from_orm(book) for book in books]
      return SearchBooksResponse(success=True, message="Books retrieved successfully", books=book_bases)
    except Exception as e:
      logger.error(f"Error searching books: {e}")
      return self.manage_error(e)

  def rent_book(self, rent_book_request: RentBookRequest):
    try:
      book = self.db.query(Book).filter(Book.id == rent_book_request.book_id).first()
      error_response = None
      if not book:
        error_response = BookResponse(success=False, message="Book not found")
      if book and book.user_id:
        error_response = BookResponse(success=False, message="The book is not available, it was rented by another user.")
      if not self.user_controller.user_exists(user_id=rent_book_request.user_id):
        error_response = BookResponse(success=False, message="User not found")
      if error_response:
        return JSONResponse(status_code=400, content=error_response.dict())
      book.user_id = rent_book_request.user_id
      self.db.commit()
      self.db.refresh(book)
      book_base = BookBase.from_orm(book)
      return BookResponse(success=True, message="Book rented successfully", book=book_base)
    except Exception as e:
      logger.error(f"Error renting book: {e}")
      self.db.rollback()
      return self.manage_error(e)

  def return_book(self, rent_book_request: RentBookRequest):
    try:
      book = self.db.query(Book).filter(Book.id == rent_book_request.book_id).first()
      error_response = None
      if not book:
        error_response = BookResponse(success=False, message="Book not found")
      if book and not book.user_id:
        error_response = BookResponse(success=False, message="The book has not been rented")
      if book and book.user_id and book.user_id != rent_book_request.user_id:
        error_response = BookResponse(success=False, message="The book was not rented by this user")
      if error_response:   
        return JSONResponse(status_code=400, content=error_response.dict())
      book.user_id = None
      self.db.commit()
      self.db.refresh(book)
      book_base = BookBase.from_orm(book)
      return BookResponse(success=True, message="Book returned successfully", book=book_base)
    except Exception as e:
      logger.error(f"Error returning book: {e}")
      self.db.rollback()
      return self.manage_error(e)