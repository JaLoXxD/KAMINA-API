import pytest
from fastapi import FastAPI, HTTPException, Request
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from app.exceptions import ExceptionHandlers
from app.dto.response.generic_response import GenericResponse

app = FastAPI()

# Add routes to trigger exceptions for testing
@app.get("/raise-http-exception")
async def raise_http_exception():
  raise HTTPException(status_code=404, detail="Item not found")

@app.get("/raise-integrity-error")
async def raise_integrity_error():
  ExceptionHandlers.raise_integrity_error("Integrity error occurred")
  
# Add custom exception handlers
app.add_exception_handler(HTTPException, ExceptionHandlers.http_exception_handler)
app.add_exception_handler(Exception, ExceptionHandlers.global_exception_handler)

client = TestClient(app)

def test_http_exception_handler():
  response = client.get("/raise-http-exception")
  assert response.status_code == 404
  data = response.json()
  assert data["success"] is False
  assert data["message"] == "Item not found"

def test_integrity_error_handler():
  response = client.get("/raise-integrity-error")
  assert response.status_code == 400
  data = response.json()
  assert data["success"] is False
  assert data["message"] == "Integrity error occurred"
