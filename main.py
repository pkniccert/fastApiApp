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

@app.post("/")
async def read_post(skip: int=0, limit: int=10):
    return {"message": "This is Post Method", "skip":skip, "limit":limit}

@app.get("/food/{food_name}")
async def get_food(food_name:foofEnum):
    if food_name is foofEnum.vegetables:
        return {"food_name": food_name, "message": "You are healthy"}
    
    if food_name.value == "fruits":
        return {"food_name": food_name, "message": "You are still healthy, but like sweet things"}
    
    return {"food_name": food_name, "message": "I like chocolate milk"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

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

@app.post("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

