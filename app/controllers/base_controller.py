from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from app.dto.response.generic_response import GenericResponse
import os

class BaseController:
  @staticmethod
  def manage_error(err: Exception):
    user_message = "An unexpected error occurred. Please try again later."
    if isinstance(err, IntegrityError):
      if "Duplicate entry" in str(err):
        user_message = "The email address is already registered. Please use a different one."
    error_response = GenericResponse(success = False, message = user_message)
    return JSONResponse(status_code=400, content=error_response.dict())