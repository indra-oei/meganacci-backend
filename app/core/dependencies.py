from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.core.response import api_response

# This tells FastAPI where clients should obtain tokens (your login endpoint).
# Swagger UI will use this when you click "Authorize".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency that extracts and validates the JWT from the Authorization header.
    Returns user info (from token payload) or raises 401 if invalid/expired.
    """
    payload = decode_access_token(token)
    if payload is None:
        return api_response(
            401,
            None,
            "Invalid or expired token"
        )
    
    # Return a minimal identity object.
    # You can extend this later to query the DB for fresh user state.
    return {
        "id": payload.get("sub"),
        "username": payload.get("username")
    }
