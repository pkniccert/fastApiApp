from sqlalchemy.ext.asyncio import AsyncSession
from config.database import engine
from models.base import Base

async def init():
    async with engine.begin() as conn:
        # Drop all tables (useful for development)
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

import asyncio
asyncio.run(init())