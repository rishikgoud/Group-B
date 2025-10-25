"""
Contract management endpoints
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import aiofiles
import os
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    """Upload a contract file for analysis"""
    
    # Validate file type
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in ["pdf", "docx", "txt", "png", "jpg", "jpeg"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, DOCX, TXT, PNG, JPG, or JPEG files."
        )
    
    # Validate file size (10MB limit)
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 10MB."
        )
    
    # Save file temporarily
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return {
            "message": "File uploaded successfully",
            "filename": filename,
            "file_path": file_path,
            "file_size": len(content),
            "file_type": file_extension
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

@router.get("/list")
async def list_contracts():
    """List all uploaded contracts"""
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        return {"contracts": []}
    
    contracts = []
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        if os.path.isfile(file_path):
            stat = os.stat(file_path)
            contracts.append({
                "filename": filename,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
    
    return {"contracts": contracts}

@router.delete("/{filename}")
async def delete_contract(filename: str):
    """Delete a contract file"""
    upload_dir = "uploads"
    file_path = os.path.join(upload_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )
    
    try:
        os.remove(file_path)
        return {"message": f"Contract {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete contract: {str(e)}"
        )
