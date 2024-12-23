from fastapi import APIRouter
from app.routes.user_routes import router as user_router
from app.routes.author_routes import router as author_router
from app.routes.book_routes import router as book_router

api_router = APIRouter()
api_router.include_router(user_router, tags=["Users"])
api_router.include_router(author_router, tags=["Authors"])
api_router.include_router(book_router, tags=["Books"])