from sqlalchemy.orm import Session
from datetime import datetime
from app.models.admin_refresh_token import AdminRefreshToken

class AdminRefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, admin_id: int, token: str, expires_at: datetime):
        rt = AdminRefreshToken(admin_id=admin_id, token=token, expires_at=expires_at)
        self.db.add(rt)
        self.db.commit()
        self.db.refresh(rt)
        return rt

    def get_valid(self, token: str):
        return (
            self.db.query(AdminRefreshToken)
            .filter(
                AdminRefreshToken.token == token,
                AdminRefreshToken.revoked == False,
                AdminRefreshToken.expires_at > datetime.now()
            )
            .first()
        )

    def revoke(self, token: str):
        rt = self.db.query(AdminRefreshToken).filter(AdminRefreshToken.token == token).first()
        if rt:
            rt.revoked = True
            self.db.commit()
        return rt

    def revoke_all(self, admin_id: int):
        self.db.query(AdminRefreshToken).filter(AdminRefreshToken.admin_id == admin_id).update({"revoked": True})
        self.db.commit()