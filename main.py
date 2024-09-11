from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import HTTPException
from routers import main_router
from middleware.auth_middleware import AuthMiddleware

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )

@app.get("/")
async def read_get():
    return {"status":"success", "message": "This is test route"}

app.add_middleware(AuthMiddleware)
# Include the main router which includes all sub-routers
app.include_router(main_router)

