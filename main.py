from enum import Enum
from fastapi import FastAPI
from routers import main_router

class foofEnum(str, Enum):
    fruits = 'fruits'
    vegetables = 'vegetables'
    dairy = 'dairy'


app = FastAPI()

# Include the main router which includes all sub-routers
app.include_router(main_router)

@app.get("/")
async def read_get():
    return {"message": "This is test route"}

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

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

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

