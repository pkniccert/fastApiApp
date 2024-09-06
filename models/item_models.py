# app/models/item_models.py

from pydantic import BaseModel

class Item(BaseModel):
    id: int
    description: str
    price: float