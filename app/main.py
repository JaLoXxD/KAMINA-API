from fastapi import FastAPI, HTTPException
from app.database import Base, engine
from app.exceptions import ExceptionHandlers
from app.routes.api import api_router

app = FastAPI()

# Initialize database
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(api_router, prefix="/api/v1")

# Register exception handlers
app.add_exception_handler(Exception, ExceptionHandlers.global_exception_handler)
app.add_exception_handler(HTTPException, ExceptionHandlers.http_exception_handler)