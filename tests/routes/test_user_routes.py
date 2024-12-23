import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.schemas.user_schema import UserBase
from app.dto.request.user_request import UserRequest
from app.dto.request.user_credentials_request import UserCredentialsRequest
from app.dto.response.user_response import UserResponse
from app.dto.response.generic_response import GenericResponse

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_user(client, setup_test_db):
  # Test creating a user
  user_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }
  response = client.post("/api/v1/users/register", json=user_data)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "User created successfully"
  assert data["user"]["name"] == "John Doe"
  assert data["user"]["email"] == "john.doe@example.com"
  assert data["user"]["register_date"] is not None

def test_login_user(client, setup_test_db):
  user_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }
  response = client.post("/api/v1/users/register", json=user_data)  
  user_data = {
    "email": "john.doe@example.com",
    "password": "password123"
  }
  response = client.post("/api/v1/users/login", json=user_data)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert "access_token" in data

def test_login_invalid_credentials(client, setup_test_db):
  user_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }
  response = client.post("/api/v1/users/register", json=user_data)  
  user_data = {
    "email": "john.doe@example.com",
    "password": "password1234"
  }
  response = client.post("/api/v1/users/login", json=user_data)
  assert response.status_code == 401
  data = response.json()
  assert data["success"] is False
  assert data["message"] == "Invalid email or password"

def test_login_invalid_email(client, setup_test_db):
  user_data = {
    "name": "John Doe",
    "email": "john.doeexample.com",
    "password": "password123"
  }
  response = client.post("/api/v1/users/register", json=user_data)  
  assert response.status_code == 400
  data = response.json()
  assert data["success"] is False
  assert data["message"] == "Invalid email"
  assert not data["user"]

def test_get_user_by_id(client, setup_test_db, auth_token):
  #REGISTER A USER FOR GET IT LATER
  user_data = {
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "password": "password123"
  }
  response = client.post("/api/v1/users/register", json=user_data)
  user_id = response.json()["user"]["id"]

  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.get(f"/api/v1/users/{user_id}", headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["user"]["name"] == "Jane Doe"
  assert data["user"]["email"] == "jane.doe@example.com"

def test_update_user_by_id(client, setup_test_db, auth_token):
  # Test updating a user
  user_data = {
    "name": "Jorge Hidalgo",
    "email": "jhidalgo512@gmail.com",
    "password": "password123"
  }
  response = client.post("/api/v1/users/register", json=user_data)
  user_id = response.json()["user"]["id"]
  updated_user_data = {
    "name": "Jorge Orlando Hidalgo",
    "email": "jhidalgo1228@gmail.com",
    "password": "password12345"
  }
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.put(f"/api/v1/users/{user_id}", json=updated_user_data, headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "User updated successfully"
  assert data["user"]["name"] == updated_user_data["name"]
  assert data["user"]["email"] == updated_user_data["email"]

def test_delete_user_by_id(client, setup_test_db, auth_token):
  user_data = {
    "name": "Dayana Q.",
    "email": "dayana24@gmail.com",
    "password": "password123"
  }
  response = client.post("/api/v1/users/register", json=user_data)
  user_id = response.json()["user"]["id"]
  headers = {"Authorization": f"Bearer {auth_token}"}
  response = client.delete(f"/api/v1/users/{user_id}", headers=headers)
  assert response.status_code == 200
  data = response.json()
  assert data["success"] is True
  assert data["message"] == "User deleted successfully"