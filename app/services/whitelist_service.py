import io
import openpyxl
from datetime import datetime
from fastapi import UploadFile

from app.repositories.whitelist_repository import WhitelistRepository
from app.models.whitelist import Whitelist
from app.models.admin import Admin

class WhitelistService:
    def __init__(self, repository: WhitelistRepository, current_user: Admin):
        self.repository = repository
        self.current_user = current_user
        print(current_user)

    def get_by_wallet_address(self, wallet_address: str):
        whitelist = self.repository.get_by_wallet_address(wallet_address)
        return whitelist
    
    async def import_whitelist(self, file: UploadFile):
        contents = await file.read()

        if not contents:
            raise ValueError("No file uploaded or file is empty")

        try:
            workbook = openpyxl.load_workbook(io.BytesIO(contents))
        except Exception as e:
            raise ValueError(f"Invalid Excel file: {str(e)}")
        
        whitelists = []
        for sheet in workbook.worksheets:
            for idx, row in enumerate(sheet.iter_rows(min_row=1, values_only=True), start=1):
                if not row[1]:
                    print(f"Null found at row {idx}: {row}")
                whitelists.append({
                    "wallet_address": row[0],
                    "whitelist_type": row[1],
                    "created_by": self.current_user['id'],
                    "created_at": datetime.now()
                })

        self.repository.add(whitelists)
        return len(whitelists)

    def export_to_excel(self):
        records = self.repository.get_all()

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Wallet Whitelist'

        sheet.append(['No', 'Wallet Address', 'Whitelist Type'])

        for idx, row in enumerate(records, start=1):
            sheet.append([idx, row.wallet_address, row.whitelist_type])

        buffer = io.BytesIO()
        workbook.save(buffer)
        buffer.seek(0)

        return buffer