from fastapi import APIRouter
from models.user_models import User

router = APIRouter()

@router.get("/list")
async def get_user_list():
    return {"message": "This is users list"}

@router.get("/me")
async def get_current_user():
    return {"message": "This is current user"}

@router.get("/{user_id}")
async def get_unique_user(user_id: int):
    return User(id=user_id, name="John Doe", email="john.doe@example.com")