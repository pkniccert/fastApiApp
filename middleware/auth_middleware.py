from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from utils.jwt import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")
            try:
                payload = verify_token(token)
            except HTTPException:
                return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        response = await call_next(request)
        return response