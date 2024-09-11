from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from utils.jwt import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract token from Authorization header
        token = request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")
            try:
                # Verify the token
                payload = verify_token(token)
                # Attach user info to request state if necessary
                request.state.user = payload
            except HTTPException as e:
                # Return JSON response with 401 Unauthorized if token verification fails
                return JSONResponse(
                    content={"status": "error", "message": str(e.detail)},
                    status_code=e.status_code
                )
            except Exception:
                # Catch any other exceptions and return a generic 401 response
                return JSONResponse(
                    content={"status": "error", "message": "User Unauthorized"},
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        
        # Proceed with the request if the token is valid or no token is present
        response = await call_next(request)
        return response
