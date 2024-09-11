from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from utils.jwt import verify_token
from schemas.user import UserInDB
from routers.base import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserInDB:
    try:
        # Verify the token and extract the payload
        payload = verify_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Query the user from the database
        query = select(User).filter(User.username == payload.get("sub"))
        result = await db.execute(query)
        user = result.scalars().first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Return user as UserInDB schema
        return UserInDB(username=user.username, password=user.password)

    except Exception as e:
        # Catch any unexpected errors and return a consistent error response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
            headers={"WWW-Authenticate": "Bearer"}
        ) from e
