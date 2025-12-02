from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import api_response

from app.services.whitelist_service import WhitelistService
from app.repositories.whitelist_repository import WhitelistRepository

router = APIRouter()

def get_whitelist_service(db: Session = Depends(get_db)):
    repository = WhitelistRepository(db)
    return WhitelistService(repository, current_user=None)

@router.get('/wallet/{wallet_address}')
def get_whitelist_by_wallet(wallet_address: str, service: WhitelistService = Depends(get_whitelist_service)):
    record = service.get_by_wallet_address(wallet_address)
    if not record:
        return api_response(404, None, "Address not found")
    return api_response(
        200, 
        {
            "wallet_address": record.wallet_address, 
            "whitelist_type": record.whitelist_type
        }, 
        f"Congratulation you're eligible for the {record.whitelist_type} whitelist"
    )