"""
Contract service for business logic
"""

from sqlalchemy.orm import Session
from app.models.database import Contract
from typing import List, Dict, Any, Optional
import aiofiles
import os
import uuid
from datetime import datetime

class ContractService:
    def __init__(self, db: Session):
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
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=len(content),
            file_type=file_extension,
            upload_date=datetime.utcnow()
        )
        
        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        
        return {
            "contract_id": contract.id,
            "filename": contract.filename,
            "file_size": contract.file_size,
            "file_type": contract.file_type,
            "upload_date": contract.upload_date
        }
    
    def get_contracts(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get list of contracts"""
        contracts = self.db.query(Contract).offset(skip).limit(limit).all()
        
        return [
            {
                "id": contract.id,
                "filename": contract.filename,
                "original_filename": contract.original_filename,
                "file_size": contract.file_size,
                "file_type": contract.file_type,
                "upload_date": contract.upload_date.isoformat(),
                "processed": contract.processed
            }
            for contract in contracts
        ]
    
    def get_contracts_count(self) -> int:
        """Get total count of contracts"""
        return self.db.query(Contract).count()
    
    def get_contract_by_id(self, contract_id: int) -> Optional[Contract]:
        """Get contract by ID"""
        return self.db.query(Contract).filter(Contract.id == contract_id).first()
    
    def delete_contract(self, contract_id: int) -> bool:
        """Delete contract and associated files"""
        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
        
        if not contract:
            return False
        
        # Delete file from filesystem
        try:
            if os.path.exists(contract.file_path):
                os.remove(contract.file_path)
        except Exception as e:
            print(f"Warning: Could not delete file {contract.file_path}: {e}")
        
        # Delete from database (cascade will handle related records)
        self.db.delete(contract)
        self.db.commit()
        
        return True
    
    def mark_contract_processed(self, contract_id: int, extracted_text: str = None) -> bool:
        """Mark contract as processed"""
        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
        
        if not contract:
            return False
        
        contract.processed = True
        if extracted_text:
            contract.extracted_text = extracted_text
        
        self.db.commit()
        return True
