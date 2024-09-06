# app/routers/item_router.py
from fastapi import APIRouter
from models.item_models import Item
from typing import Union

router = APIRouter()

@router.get("/optional/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router.post("/optional/param")
async def read_post(skip: int | None = None, limit: int | None = None):
    return {"message": "This is Post Method", "skip":skip, "limit": limit}

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    return Item(id=item_id, description="A cool item", price=19.99)