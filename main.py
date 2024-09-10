from fastapi import FastAPI
from routers import main_router
from middleware.auth_middleware import AuthMiddleware

app = FastAPI()

@app.get("/")
async def read_get():
    return {"message": "This is test route"}

# app.add_middleware(AuthMiddleware)
# Include the main router which includes all sub-routers
app.include_router(main_router)

