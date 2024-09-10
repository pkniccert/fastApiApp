from config.database import AsyncSessionLocal
# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session