from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from routers.base import get_db
from models import Item

router = APIRouter()

@router.post("/items/")
async def create_item(name: str, description: str, db: AsyncSession = Depends(get_db)):
    item = Item(name=name, description=description)
    db.add(item)
    await db.commit()
    return item

@router.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(item).filter(item.id == item_id))
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item