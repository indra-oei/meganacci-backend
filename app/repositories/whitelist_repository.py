from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.whitelist import Whitelist

class WhitelistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Whitelist).all()

    def get_by_wallet_address(self, wallet_address: str):
        return self.db.query(Whitelist).filter(Whitelist.wallet_address == wallet_address).first()
    
    def add(self, whitelists: list[dict]):
        stmt = insert(Whitelist).values(whitelists)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=['wallet_address']
        )
        self.db.execute(stmt)
        self.db.commit()