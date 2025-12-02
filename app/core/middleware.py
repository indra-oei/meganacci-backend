from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import decode_access_token
from app.core.response import api_response

class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only protect admin routes
        path = request.url.path
        if path.startswith("/v1/admin") and not path.endswith("/login"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return api_response(401, None, "Missing or invalid Authorization header")

            token = auth_header.split(" ")[1]
            payload = decode_access_token(token)
            if payload is None:
                return api_response(401, None, "Invalid or expired token")

            # Attach admin info to request.state for downstream use
            request.state.admin = payload.get("sub")

        # Continue request flow
        return await call_next(request)
