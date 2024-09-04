from typing import Union
from enum import Enum
from fastapi import FastAPI

class foofEnum(str, Enum):
    fruits = 'fruits'
    vegetables = 'vegetables'
    dairy = 'dairy'


app = FastAPI()


@app.get("/")
async def read_get():
    return {"message": "This is Get Route"}

@app.put("/")
async def read_put():
    return {"message": "This is Put Method"}

@app.get("/food/{food_name}")
async def get_food(food_name:foofEnum):
    if food_name is foofEnum.vegetables:
        return {"food_name": food_name, "message": "You are healthy"}
    
    if food_name.value == "fruits":
        return {"food_name": food_name, "message": "You are still healthy, but like sweet things"}
    
    return {"food_name": food_name, "message": "I like chocolate milk"}

@app.post("/")
async def read_post(skip: int=0, limit: int=10):
    return {"message": "This is Post Method", "skip":skip, "limit":limit}

@app.post("/optional/param")
async def read_post(skip: int | None = None, limit: int | None = None):
    return {"message": "This is Post Method", "skip":skip, "limit": limit}

@app.get("/users/list")
async def get_user_list():
    return {"message": "This is users list"}

@app.get("/users/me")
async def get_current_user():
    return {"message": "This is current user"}

@app.get("/users/{user_id}")
async def get_unique_user(user_id: str):
    return {"message": "This is unique user", "UserId":user_id}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

