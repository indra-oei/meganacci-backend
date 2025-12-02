from datetime import datetime, timedelta
from app.repositories.admin_repository import AdminRepository
from app.repositories.admin_refresh_token_repository import AdminRefreshTokenRepository
from app.models.admin import Admin

class AuthService:
    def __init__(self, admin_repo: AdminRepository, refresh_repo: AdminRefreshTokenRepository, verify_password_fn, create_token_fn, create_refresh_token_fn):
        self.admin_repo = admin_repo
        self.refresh_repo = refresh_repo
        self.verify_password = verify_password_fn
        self.create_token = create_token_fn
        self.create_refresh_token = create_refresh_token_fn
    
    def authenticate(self, username: str, password: str):
        admin = self.admin_repo.get_by_username(username)
        if not admin or not self.verify_password(password, admin.password):
            return None
        return admin

    def generate_access_token(self, admin: Admin, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        return self.create_token(
            {"sub": str(admin.id), "username": admin.username},
            expires_delta=expires_delta
        )

    def generate_refresh_token(self, admin: Admin, expires_delta: timedelta = timedelta(days=7)) -> str:
        refresh_token = self.create_refresh_token(
            {"sub": str(admin.id), "username": admin.username},
            expires_delta=expires_delta
        )
        # Persist refresh token in DB
        self.refresh_repo.create(admin.id, refresh_token, datetime.utcnow() + expires_delta)
        return refresh_token

    def refresh_access_token(self, refresh_token: str) -> str | None:
        rt = self.refresh_repo.get_valid(refresh_token)
        if not rt:
            return None
        payload = self.create_token.decode(refresh_token)  # depends on your JWT helper
        admin_id = int(payload["sub"])
        return self.generate_access_token(Admin(id=admin_id, username=payload["username"]))

    def logout(self, admin_id: int):
        self.refresh_repo.revoke_all(admin_id)
        return {"message": "Logged out successfully"}