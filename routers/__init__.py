# app/routers/__init__.py

from fastapi import APIRouter
from .user_router import router as user_router
from .item_router import router as item_router
from .admin_router import router as admin_router

# Create a main router to include all routers
main_router = APIRouter()

# Include all sub-routers
main_router.include_router(user_router, prefix="/users", tags=["users"])
main_router.include_router(item_router, prefix="/items", tags=["items"])
main_router.include_router(admin_router, prefix="/admin", tags=["admin"])