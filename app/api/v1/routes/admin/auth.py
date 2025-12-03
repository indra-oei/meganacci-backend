from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.database import get_db
from app.core.response import api_response
from app.core.dependencies import get_current_user

from app.services.auth_service import AuthService
from app.repositories.admin_repository import AdminRepository
from app.repositories.admin_refresh_token_repository import AdminRefreshTokenRepository

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)):
    admin_repo = AdminRepository(db)
    refresh_repo = AdminRefreshTokenRepository(db)
    return AuthService(admin_repo, refresh_repo, verify_password, create_access_token, create_refresh_token)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(get_auth_service)):
    admin = service.authenticate(form_data.username, form_data.password)
    if not admin:
        return api_response(401, None, "Invalid credentials")
    
    token = service.generate_access_token(admin)
    return api_response(
        200, 
        {
            "access_token": token, 
            "token_type": "bearer"
        }, 
        "Login successful"
    )

@router.post("/refresh")
def refresh_token(refresh_token: str, service: AuthService = Depends(get_auth_service)):
    new_access_token = service.refresh_access_token(refresh_token)
    if not new_access_token:
        return api_response(401, None, "Invalid or expired refresh token")
    return api_response(
        200,
        {"access_token": new_access_token, "token_type": "bearer"},
        "Token refreshed"
    )

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return api_response(200, current_user, "Current user retrieved")