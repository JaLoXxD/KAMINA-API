from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from app.dto.response.genericResponse import GenericResponse
import os

class BaseController:
  @staticmethod
  def manageError(err: Exception):
    # Default user-friendly message
    user_message = "An unexpected error occurred. Please try again later."
    
    # Handle specific errors (e.g., IntegrityError)
    if isinstance(err, IntegrityError):
      if "Duplicate entry" in str(err):
        user_message = "The email address is already registered. Please use a different one."

    # Construct the response
    errorResponse = GenericResponse(success = False, message = user_message)
    return JSONResponse(status_code=400, content=errorResponse.dict())