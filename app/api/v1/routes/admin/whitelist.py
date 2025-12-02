from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.response import api_response
from app.core.dependencies import get_current_user

from app.services.whitelist_service import WhitelistService
from app.repositories.whitelist_repository import WhitelistRepository
from app.models.admin import Admin

router = APIRouter()

def get_whitelist_service(db: Session = Depends(get_db), current_user: Admin = Depends(get_current_user)):
    repository = WhitelistRepository(db)
    return WhitelistService(repository, current_user)

@router.post('/import')
async def import_whitelist(file: UploadFile = File(...), service: WhitelistService = Depends(get_whitelist_service)):
    try:
        whitelist_count = await service.import_whitelist(file)
        return api_response(200, {"count": whitelist_count}, "Import successful")
    except ValueError as e:
        return api_response(400, None, str(e))

@router.get('/export')
def export_whitelist(service: WhitelistService = Depends(get_whitelist_service)):
    buffer = service.export_to_excel()

    filename = f"whitelist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )