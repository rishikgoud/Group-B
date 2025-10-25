"""
Contract upload routes
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import aiofiles
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models.schemas import ContractUploadResponse, ContractListResponse, ContractDetailResponse
from services.contract_service import ContractService

router = APIRouter()

@router.post("/upload", response_model=ContractUploadResponse)
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a contract file for analysis"""
    
    # Validate file type
    file_extension = file.filename.split('.')[-1].lower()
    allowed_types = ["pdf", "docx", "txt", "png", "jpg", "jpeg"]
    if file_extension not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Please upload: {', '.join(allowed_types)} files."
        )
    
    # Validate file size (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 10MB."
        )
    
    try:
        # Use contract service to handle upload
        contract_service = ContractService(db)
        result = await contract_service.upload_contract(file)
        
        return ContractUploadResponse(
            contract_id=result["contract_id"],
            filename=result["filename"],
            file_size=result["file_size"],
            file_type=result["file_type"],
            upload_date=result["upload_date"],
            message="Contract uploaded successfully"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload contract: {str(e)}"
        )

@router.get("/list", response_model=ContractListResponse)
async def list_contracts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all uploaded contracts"""
    try:
        contract_service = ContractService(db)
        contracts = contract_service.get_contracts(skip=skip, limit=limit)
        total_count = contract_service.get_contracts_count()
        
        return ContractListResponse(
            contracts=contracts,
            total_count=total_count
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve contracts: {str(e)}"
        )

@router.get("/{contract_id}", response_model=ContractDetailResponse)
async def get_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific contract"""
    try:
        contract_service = ContractService(db)
        contract = contract_service.get_contract_by_id(contract_id)
        
        if not contract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )
        
        return ContractDetailResponse(
            id=contract.id,
            filename=contract.filename,
            original_filename=contract.original_filename,
            file_size=contract.file_size,
            file_type=contract.file_type,
            upload_date=contract.upload_date,
            processed=contract.processed,
            analyses=[{
                "id": analysis.id,
                "analysis_type": analysis.analysis_type,
                "overall_risk_score": analysis.overall_risk_score,
                "total_clauses": analysis.total_clauses,
                "analysis_date": analysis.analysis_date
            } for analysis in contract.analyses]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve contract: {str(e)}"
        )

@router.delete("/{contract_id}")
async def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Delete a contract and its associated data"""
    try:
        contract_service = ContractService(db)
        success = contract_service.delete_contract(contract_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )
        
        return {"message": f"Contract {contract_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete contract: {str(e)}"
        )
