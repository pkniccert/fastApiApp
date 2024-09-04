from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_get():
    return {"message": "This is Get Route"}

@app.put("/")
async def read_put():
    return {"message": "This is Put Method"}

@app.post("/")
async def read_post():
    return {"message": "This is Post Method"}

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

