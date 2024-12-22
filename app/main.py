from fastapi import FastAPI, HTTPException
from app.database import Base, engine
from app.routes.userRoutes import router as user_router
from app.exceptions import ExceptionHandlers

app = FastAPI()

# Initialize database
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(user_router, prefix="/api/v1", tags=["Users"])

# Register exception handlers
app.add_exception_handler(Exception, ExceptionHandlers.global_exception_handler)
app.add_exception_handler(HTTPException, ExceptionHandlers.http_exception_handler)