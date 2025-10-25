"""
Dataset endpoints for querying Kaggle Contracts Clauses Dataset
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.models.database import Clause
from app.models.schemas import ClauseResponse, ClauseListResponse
from services.dataset_loader import DatasetLoaderService
from beanie import PydanticObjectId

router = APIRouter()

@router.get("/clauses", response_model=ClauseListResponse)
async def get_clauses(
    clause_type: Optional[str] = Query(None, description="Filter by clause type"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    search_text: Optional[str] = Query(None, description="Search in clause text"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """Get clauses from the dataset with optional filtering"""
    try:
        loader = DatasetLoaderService()

        # Calculate offset
        offset = (page - 1) * page_size

        # Search clauses using DatasetLoaderService (async)
        clauses = await loader.search_clauses(
            search_text=search_text,
            clause_type=clause_type,
            risk_level=risk_level,
            skip=offset,
            limit=page_size
        )

        # Get total count for pagination
        total_count = await loader.get_clauses_count()

        # Convert to response format
        clause_responses = [
            ClauseResponse(
                id=str(clause.id),
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
async def get_clause_by_id(clause_id: str):
    """Get a specific clause by ID"""
    try:
        clause = await Clause.get(PydanticObjectId(clause_id))
        if not clause or clause.source_dataset != "kaggle_contracts_clauses":
            raise HTTPException(status_code=404, detail="Clause not found")

        return ClauseResponse(
            id=str(clause.id),
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
        raise HTTPException(status_code=500, detail=f"Failed to retrieve clause: {str(e)}")


@router.get("/clauses/types/list")
async def get_clause_types():
    """Get list of available clause types"""
    try:
        clause_types = await Clause.find(
            {"source_dataset": "kaggle_contracts_clauses"}
        ).distinct("clause_type")

        return {"clause_types": clause_types, "total_types": len(clause_types)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve clause types: {str(e)}")


@router.get("/clauses/risk-levels/list")
async def get_risk_levels():
    """Get list of available risk levels"""
    try:
        risk_levels = await Clause.find(
            {"source_dataset": "kaggle_contracts_clauses", "risk_level": {"$ne": None}}
        ).distinct("risk_level")

        return {"risk_levels": risk_levels, "total_levels": len(risk_levels)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve risk levels: {str(e)}")


@router.get("/dataset/stats")
async def get_dataset_stats():
    """Get dataset statistics"""
    try:
        loader = DatasetLoaderService()
        total_clauses = await loader.get_clauses_count()

        # Clause type distribution
        clause_types = await Clause.find({"source_dataset": "kaggle_contracts_clauses"}).distinct("clause_type")
        type_distribution = {}
        for clause_type in clause_types:
            count = await Clause.find(
                {"clause_type": clause_type, "source_dataset": "kaggle_contracts_clauses"}
            ).count()
            type_distribution[clause_type] = count

        # Risk level distribution
        risk_levels = await Clause.find(
            {"source_dataset": "kaggle_contracts_clauses", "risk_level": {"$ne": None}}
        ).distinct("risk_level")
        risk_distribution = {}
        for risk_level in risk_levels:
            count = await Clause.find(
                {"risk_level": risk_level, "source_dataset": "kaggle_contracts_clauses"}
            ).count()
            risk_distribution[risk_level] = count

        return {
            "total_clauses": total_clauses,
            "clause_type_distribution": type_distribution,
            "risk_level_distribution": risk_distribution,
            "dataset_source": "kaggle_contracts_clauses"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dataset stats: {str(e)}")


@router.post("/dataset/reload")
async def reload_dataset():
    """Reload the dataset (admin endpoint)"""
    try:
        loader = DatasetLoaderService()

        # Clear existing dataset
        await Clause.find({"source_dataset": "kaggle_contracts_clauses"}).delete_many()

        # Reload dataset
        success = await loader.load_dataset_to_db()

        if success:
            count = await loader.get_clauses_count()
            return {"message": "Dataset reloaded successfully", "total_clauses": count}
        else:
            raise HTTPException(status_code=500, detail="Failed to reload dataset")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload dataset: {str(e)}")
