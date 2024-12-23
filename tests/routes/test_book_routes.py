import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.schemas.user_schema import UserBase
from app.dto.request.user_request import UserRequest
from app.dto.request.user_credentials_request import UserCredentialsRequest
from app.dto.request.book_request import BookRequest
from app.dto.request.rent_book_request import RentBookRequest
from app.dto.response.user_response import UserResponse
from app.dto.response.book_response import BookResponse
from app.dto.response.search_books_response import SearchBooksResponse
from app.dto.response.generic_response import GenericResponse

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_book(client, setup_test_db, auth_token):
  # Create an author first
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]

  # Test creating a book
  book_data = {
    "title": "Harry Potter and the Philosopher's Stone",
    "published_year": 1997,
    "author_id": author_id
  }
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Book created successfully"
  assert data["book"]["title"] == "Harry Potter and the Philosopher's Stone"
  assert data["book"]["published_year"] == 1997

def test_get_book_by_id(client, setup_test_db, auth_token):
  # Create an author first
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]

  # Create a book
  book_data = {
    "title": "Harry Potter and the Goblet of Fire",
    "published_year": 2000,
    "author_id": author_id
  }
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  book_id = response.json()["book"]["id"]

  # Test retrieving the book by ID
  response = client.get(f"/api/v1/books/{book_id}", headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Book retrieved successfully"
  assert data["book"]["title"] == "Harry Potter and the Goblet of Fire"
  assert data["book"]["published_year"] == 2000

def create_author(client, auth_token):
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  return response.json()["author"]["id"]

def create_book(client, auth_token, author_id, title, published_year):
  book_data = {
    "title": title,
    "published_year": published_year,
    "author_id": author_id
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  return response.json()["book"]["id"]

def test_update_book(client, setup_test_db, auth_token):
  # Create an author first
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]

  # Create a book
  book_data = {
    "title": "Harry Potter and the Order of the Phoenix",
    "published_year": 2003,
    "author_id": author_id
  }
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  book_id = response.json()["book"]["id"]

  # Test updating the book
  updated_book_data = {
    "title": "Harry Potter and the Order of the Phoenix (Updated)",
    "published_year": 2003,
    "author_id": author_id
  }
  response = client.put(f"/api/v1/books/{book_id}", json=updated_book_data, headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Book updated successfully"
  assert data["book"]["title"] == "Harry Potter and the Order of the Phoenix (Updated)"
  assert data["book"]["published_year"] == 2003

def test_delete_book(client, setup_test_db, auth_token):
  # Create an author first
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]

  # Create a book
  book_data = {
    "title": "Harry Potter and the Half-Blood Prince",
    "published_year": 2005,
    "author_id": author_id
  }
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  book_id = response.json()["book"]["id"]

  # Test deleting the book
  response = client.delete(f"/api/v1/books/{book_id}", headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Book deleted successfully"

def test_search_books(client, setup_test_db, auth_token):
  # Create an author first
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]

  # Create a book
  book_data = {
    "title": "Harry Potter and the Half-Blood Prince",
    "published_year": 2005,
    "author_id": author_id
  }
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  response = client.get("/api/v1/books/search?title=Harry Potter", headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert len(data["books"]) > 0

def test_rent_book(client, setup_test_db, auth_token):
  # Create an author first
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]

  # Create a book
  book_data = {
    "title": "Harry Potter and the Chamber of Secrets",
    "published_year": 1998,
    "author_id": author_id
  }
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  book_id = response.json()["book"]["id"]

  # Test renting a book
  rent_book_data = {
    "book_id": book_id,
    "user_id": 1  # Assuming the user ID is 1
  }
  response = client.post("/api/v1/books/rent", json=rent_book_data, headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Book rented successfully"

def test_return_book(client, setup_test_db, auth_token):
  # Create an author first
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]

  # Create a book
  book_data = {
    "title": "Harry Potter and the Prisoner of Azkaban",
    "published_year": 1999,
    "author_id": author_id
  }
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  book_id = response.json()["book"]["id"]

  # Rent the book first
  rent_book_data = {
    "book_id": book_id,
    "user_id": 1  # Assuming the user ID is 1
  }
  response = client.post("/api/v1/books/rent", json=rent_book_data, headers=headers)

  # Test returning the book
  response = client.post("/api/v1/books/return", json=rent_book_data, headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Book returned successfully"

def test_get_book_by_id(client, setup_test_db, auth_token):
  # Create an author first
  author_data = {
    "name": "J.K. Rowling",
    "birth_date": "31/07/1965"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]

  # Create a book
  book_data = {
    "title": "Harry Potter and the Goblet of Fire",
    "published_year": 2000,
    "author_id": author_id
  }
  response = client.post("/api/v1/books/", json=book_data, headers=headers)
  book_id = response.json()["book"]["id"]

  # Test retrieving the book by ID
  response = client.get(f"/api/v1/books/{book_id}", headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Book retrieved successfully"
  assert data["book"]["title"] == "Harry Potter and the Goblet of Fire"
  assert data["book"]["published_year"] == 2000