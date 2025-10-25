"""
Dataset endpoints for querying Kaggle Contracts Clauses Dataset
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.schemas import (
    ClauseResponse, 
    ClauseListResponse, 
    ClauseSearchRequest
)
from services.dataset_loader import DatasetLoaderService

router = APIRouter()

@router.get("/clauses", response_model=ClauseListResponse)
async def get_clauses(
    clause_type: Optional[str] = Query(None, description="Filter by clause type"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    search_text: Optional[str] = Query(None, description="Search in clause text"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get clauses from the dataset with optional filtering"""
    try:
        loader = DatasetLoaderService(db)
        
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Search clauses
        clauses = loader.search_clauses(
            search_text=search_text,
            clause_type=clause_type,
            risk_level=risk_level,
            limit=page_size
        )
        
        # Get total count for pagination
        total_count = loader.get_clauses_count()
        
        # Convert to response format
        clause_responses = [
            ClauseResponse(
                id=clause.id,
                clause_type=clause.clause_type,
                text=clause.text,
                simplified_text=clause.simplified_text,
                risk_level=clause.risk_level,
                source_dataset=clause.source_dataset,
                created_at=clause.created_at
            )
            for clause in clauses
        ]
        
        return ClauseListResponse(
            clauses=clause_responses,
            total_count=total_count,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve clauses: {str(e)}"
        )

@router.get("/clauses/{clause_id}", response_model=ClauseResponse)
async def get_clause_by_id(
    clause_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific clause by ID"""
    try:
        from app.models.database import Clause
        
        clause = db.query(Clause).filter(
            Clause.id == clause_id,
            Clause.source_dataset == "kaggle_contracts_clauses"
        ).first()
        
        if not clause:
            raise HTTPException(
                status_code=404,
                detail="Clause not found"
            )
        
        return ClauseResponse(
            id=clause.id,
            clause_type=clause.clause_type,
            text=clause.text,
            simplified_text=clause.simplified_text,
            risk_level=clause.risk_level,
            source_dataset=clause.source_dataset,
            created_at=clause.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve clause: {str(e)}"
        )

@router.get("/clauses/types/list")
async def get_clause_types(db: Session = Depends(get_db)):
    """Get list of available clause types"""
    try:
        from app.models.database import Clause
        
        clause_types = db.query(Clause.clause_type).filter(
            Clause.source_dataset == "kaggle_contracts_clauses"
        ).distinct().all()
        
        return {
            "clause_types": [clause_type[0] for clause_type in clause_types],
            "total_types": len(clause_types)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve clause types: {str(e)}"
        )

@router.get("/clauses/risk-levels/list")
async def get_risk_levels(db: Session = Depends(get_db)):
    """Get list of available risk levels"""
    try:
        from app.models.database import Clause
        
        risk_levels = db.query(Clause.risk_level).filter(
            Clause.source_dataset == "kaggle_contracts_clauses",
            Clause.risk_level.isnot(None)
        ).distinct().all()
        
        return {
            "risk_levels": [risk_level[0] for risk_level in risk_levels],
            "total_levels": len(risk_levels)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve risk levels: {str(e)}"
        )

@router.get("/dataset/stats")
async def get_dataset_stats(db: Session = Depends(get_db)):
    """Get dataset statistics"""
    try:
        loader = DatasetLoaderService(db)
        
        total_clauses = loader.get_clauses_count()
        
        # Get clause type distribution
        from app.models.database import Clause
        clause_types = db.query(Clause.clause_type).filter(
            Clause.source_dataset == "kaggle_contracts_clauses"
        ).distinct().all()
        
        type_distribution = {}
        for clause_type in clause_types:
            count = db.query(Clause).filter(
                Clause.clause_type == clause_type[0],
                Clause.source_dataset == "kaggle_contracts_clauses"
            ).count()
            type_distribution[clause_type[0]] = count
        
        # Get risk level distribution
        risk_levels = db.query(Clause.risk_level).filter(
            Clause.source_dataset == "kaggle_contracts_clauses",
            Clause.risk_level.isnot(None)
        ).distinct().all()
        
        risk_distribution = {}
        for risk_level in risk_levels:
            count = db.query(Clause).filter(
                Clause.risk_level == risk_level[0],
                Clause.source_dataset == "kaggle_contracts_clauses"
            ).count()
            risk_distribution[risk_level[0]] = count
        
        return {
            "total_clauses": total_clauses,
            "clause_type_distribution": type_distribution,
            "risk_level_distribution": risk_distribution,
            "dataset_source": "kaggle_contracts_clauses"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve dataset stats: {str(e)}"
        )

@router.post("/dataset/reload")
async def reload_dataset(db: Session = Depends(get_db)):
    """Reload the dataset (admin endpoint)"""
    try:
        loader = DatasetLoaderService(db)
        
        # Clear existing dataset
        from app.models.database import Clause
        db.query(Clause).filter(
            Clause.source_dataset == "kaggle_contracts_clauses"
        ).delete()
        db.commit()
        
        # Reload dataset
        success = loader.load_dataset_to_db()
        
        if success:
            count = loader.get_clauses_count()
            return {
                "message": f"Dataset reloaded successfully",
                "total_clauses": count
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to reload dataset"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reload dataset: {str(e)}"
        )
