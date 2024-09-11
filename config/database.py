from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:PKNic%40321@127.0.0.1:5432/test_db"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)