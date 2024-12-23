import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.author import Author
from app.schemas.author_schema import AuthorBase
from app.dto.request.author_request import AuthorRequest
from app.dto.response.author_response import AuthorResponse

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_author(client, setup_test_db, auth_token):
    author_data = {
        "name": "J.R.R. Tolkien",
        "birth_date": "03/01/1892"
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/api/v1/authors/", json=author_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Author created successfully"
    assert data["author"]["name"] == "J.R.R. Tolkien"
    assert data["author"]["birth_date"] == "03/01/1892"

def test_get_author_by_id(client, setup_test_db, auth_token):
  author_data = {
    "name": "J.R.R. Tolkien",
    "birth_date": "03/01/1892"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]
  response = client.get(f"/api/v1/authors/{author_id}", headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Author retrieved successfully"
  assert data["author"]["name"] == "J.R.R. Tolkien"
  assert data["author"]["birth_date"] == "03/01/1892"

def test_update_author(client, setup_test_db, auth_token):
  author_data = {
    "name": "J.R.R. Tolkien",
    "birth_date": "03/01/1892"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]
  updated_author_data = {
    "name": "John Ronald Reuel Tolkien",
    "birth_date": "03/01/1892"
  }
  response = client.put(f"/api/v1/authors/{author_id}", json=updated_author_data, headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Author updated successfully"
  assert data["author"]["name"] == "John Ronald Reuel Tolkien"
  assert data["author"]["birth_date"] == "03/01/1892"

def test_delete_author(client, setup_test_db, auth_token):
  author_data = {
    "name": "J.R.R. Tolkien",
    "birth_date": "03/01/1892"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.post("/api/v1/authors/", json=author_data, headers=headers)
  author_id = response.json()["author"]["id"]
  response = client.delete(f"/api/v1/authors/{author_id}", headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "Author deleted successfully"