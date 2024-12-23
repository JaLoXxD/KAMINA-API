import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the `get_db` dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Define the `client` fixture
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

# Setup test database
@pytest.fixture(scope="function")
def setup_test_db():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

# Auth token fixture
@pytest.fixture(scope="function")
def auth_token(client, setup_test_db):
    user_data = {
        "name": "Test User",
        "email": "test.user@example.com",
        "password": "password123"
    }
    client.post("/api/v1/users/register", json=user_data)

    login_data = {
        "email": "test.user@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/users/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]