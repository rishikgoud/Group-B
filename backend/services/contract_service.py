"""
Contract service for business logic
"""

from app.models.mongodb_models import Contract
from typing import List, Dict, Any, Optional
import aiofiles
import os
import uuid
from datetime import datetime

class ContractService:
    def __init__(self, db):
        self.db = db
    
    async def upload_contract(self, file) -> Dict[str, Any]:
        """Upload and save contract file"""
        
        # Create uploads directory
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Create database record
        contract = Contract(
            title=file.filename,
            file_name=file.filename,
            file_path=file_path,
            file_size=len(content),
            file_type=file_extension,
            uploaded_at=datetime.utcnow()
        )
        
        await contract.insert()
        
        return {
            "contract_id": str(contract.id),
            "filename": contract.file_name,
            "file_size": contract.file_size,
            "file_type": contract.file_type,
            "upload_date": contract.uploaded_at
        }
    
    async def get_contracts(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get list of contracts"""
        contracts = await Contract.find().skip(skip).limit(limit).to_list()
        
        return [
            {
                "id": str(contract.id),
                "filename": contract.file_name,
                "original_filename": contract.file_name,
                "file_size": contract.file_size,
                "file_type": contract.file_type,
                "upload_date": contract.uploaded_at.isoformat(),
                "processed": contract.processed
            }
            for contract in contracts
        ]
    
    async def get_contracts_count(self) -> int:
        """Get total count of contracts"""
        return await Contract.count()
    
    async def get_contract_by_id(self, contract_id: str) -> Optional[Contract]:
        """Get contract by ID"""
        return await Contract.get(contract_id)
    
    async def delete_contract(self, contract_id: str) -> bool:
        """Delete contract and associated files"""
        contract = await Contract.get(contract_id)
        
        if not contract:
            return False
        
        # Delete file from filesystem
        try:
            if os.path.exists(contract.file_path):
                os.remove(contract.file_path)
        except Exception as e:
            print(f"Warning: Could not delete file {contract.file_path}: {e}")
        
        # Delete from database
        await contract.delete()
        
        return True
    
    async def mark_contract_processed(self, contract_id: str, extracted_text: str = None) -> bool:
        """Mark contract as processed"""
        contract = await Contract.get(contract_id)
        
        if not contract:
            return False
        
        contract.processed = True
        if extracted_text:
            contract.extracted_text = extracted_text
        
        await contract.save()
        return True
