from fastapi import APIRouter, Depends, HTTPException, Query
from app.dto import *
from app.controllers.book_controller import BookController
from app.controllers.token_controller import TokenController
import logging

router = APIRouter(prefix="/books")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("booksApi")

@router.post("/", response_model = BookResponse)
def create_book(book: BookRequest, controller: BookController = Depends(BookController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.create_book(book)

@router.get("/search", response_model=SearchBooksResponse)
def search_books(title: str = Query(None), authorName: str = Query(None), publishedYear: int = Query(None), controller: BookController = Depends(BookController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.search_books(title, authorName, publishedYear)

@router.post("/rent", response_model=BookResponse)
def rent_book(rentBookRequest: RentBookRequest, controller: BookController = Depends(BookController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.rent_book(rentBookRequest)

@router.post("/return", response_model=BookResponse)
def return_book(rentBookRequest: RentBookRequest, controller: BookController = Depends(BookController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.return_book(rentBookRequest)

@router.get("/{id}", response_model = BookResponse)
def get_book_by_id(id: int, controller: BookController = Depends(BookController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.get_book_by_id(id)

@router.put("/{id}", response_model=BookResponse)
def update_book_by_id(id: int, book: BookRequest, controller: BookController = Depends(BookController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.update_book_by_id(id, book)

@router.delete("/{id}", response_model=GenericResponse)
def delete_Book_by_id(id: int, controller: BookController = Depends(BookController), current_user: dict = Depends(TokenController.get_current_user)):
  return controller.delete_book_by_id(id)
