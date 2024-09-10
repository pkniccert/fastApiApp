# app/routers/__init__.py
from fastapi import APIRouter
from .user import router as user
from .item import router as item
from .admin import router as admin

# Create a main router to include all routers
main_router = APIRouter()

# Include all sub-routers
main_router.include_router(user, prefix="/users", tags=["users"])
main_router.include_router(item, prefix="/items", tags=["items"])
main_router.include_router(admin, prefix="/admin", tags=["admin"])