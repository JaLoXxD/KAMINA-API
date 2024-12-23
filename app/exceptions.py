from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.dto.response.generic_response import GenericResponse
import logging

# Configure logging
logger = logging.getLogger("exceptions")
logging.basicConfig(level=logging.INFO)

class ExceptionHandlers:
  #Class to define custom exception handlers.

  @staticmethod
  async def global_exception_handler(request: Request, exc: Exception):
    #Handle unexpected exceptions.
    logger.error(f"Unhandled exception occurred: {exc}")
    errorResponse = GenericResponse(success= False, message= str(exc))
    return JSONResponse(
      status_code=500,
      content= errorResponse.dict(),
    )

  @staticmethod
  async def http_exception_handler(request: Request, exc: HTTPException):
    #Handle HTTPExceptions with custom response.
    logger.warning(f"HTTP exception occurred: {exc.detail}")
    return JSONResponse(
      status_code=exc.status_code,
      content=exc.detail if isinstance(exc.detail, dict) else {"success": False, "message": exc.detail},
    )

  @staticmethod
  def raise_integrity_error(detail: str):
    #Raise a custom HTTPException for database integrity errors.
    errorResponse = GenericResponse(success= False, message= detail)
    raise HTTPException(
      status_code=400,
      detail= errorResponse.dict()
    )