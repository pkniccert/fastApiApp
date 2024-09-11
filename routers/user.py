from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from routers.base import get_db
from dependencies.auth import get_current_user
from models import User
from utils.jwt import create_access_token
from schemas.user import UserCreate, UserInDB
from passlib.context import CryptContext
from typing import Dict

router = APIRouter()

# Create an instance of CryptContext with bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login")
async def login(form_data: UserCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    try:
        query = select(User).filter(User.username == form_data.username)
        result = await db.execute(query)
        user = result.scalars().first()

        if user is None or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create and return access token
        access_token = create_access_token(data={"sub": form_data.username})
        return {"status": "success", "access_token": access_token, "token_type": "bearer"}

    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    except Exception as e:
        # Handle other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

@router.get("/me")
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return {"status": "success", "data": current_user}

@router.post("/create")
async def create_user(name: str, email: str, username: str, password: str, db: AsyncSession = Depends(get_db)):
    try:
        user = User(name=name, email=email, username=username, password=pwd_context.hash(password))
        db.add(user)
        await db.commit()
        return {"status": "success", "data": user}
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

@router.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return {"status": "success", "data": user}
    except SQLAlchemyError as e:
        # Handle SQLAlchemy-related exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        ) from e
