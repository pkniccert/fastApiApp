from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from routers.base import get_db
from models import User
from utils.jwt import create_access_token
from schemas.user import UserCreate, UserInDB
from sqlalchemy.orm import Session
from dependencies.auth import get_current_user
from passlib.context import CryptContext

router = APIRouter()

# Create an instance of CryptContext with bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
async def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)

@router.get("/me")
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

@router.post("/create")
async def create_user(name: str, email: str, username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = User(name=name, email=email, username=username, password=pwd_context.hash(password))
    db.add(user)
    await db.commit()
    return user

@router.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user