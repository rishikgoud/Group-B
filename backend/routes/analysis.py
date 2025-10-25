"""
Contract analysis routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.schemas import (
    AnalysisRequest, 
    ContractAnalysisResponse, 
    RiskLevelsResponse, 
    ClauseTypesResponse
)
from services.analyzer_service import AnalyzerService

router = APIRouter()

@router.post("/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze a contract and extract insights"""
    try:
        analyzer_service = AnalyzerService(db)
        result = await analyzer_service.analyze_contract(
            contract_id=request.contract_id,
            analysis_type=request.analysis_type
        )
        
        return ContractAnalysisResponse(
            contract_id=request.contract_id,
            analysis_id=result["analysis_id"],
            total_clauses=result["total_clauses"],
            risk_summary=result["risk_summary"],
            clauses=result["clauses"],
            overall_risk_score=result["overall_risk_score"],
            key_insights=result["key_insights"],
            analysis_date=result["analysis_date"],
            message="Contract analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze contract: {str(e)}"
        )

@router.get("/risk-levels", response_model=RiskLevelsResponse)
async def get_risk_levels():
    """Get available risk levels and their descriptions"""
    return RiskLevelsResponse(
        risk_levels={
            "high": {
                "description": "High risk clauses that require immediate attention",
                "color": "#ef4444",
                "examples": ["Unlimited liability", "Broad IP assignment", "Restrictive non-compete"]
            },
            "medium": {
                "description": "Moderate risk clauses that should be reviewed",
                "color": "#f59e0b",
                "examples": ["Confidentiality obligations", "Termination conditions", "Payment terms"]
            },
            "low": {
                "description": "Low risk clauses that are generally acceptable",
                "color": "#10b981",
                "examples": ["Standard definitions", "Governing law", "Basic obligations"]
            }
        }
    )

@router.get("/clause-types", response_model=ClauseTypesResponse)
async def get_clause_types():
    """Get available clause types for classification"""
    return ClauseTypesResponse(
        clause_types=[
            "confidentiality",
            "intellectual_property",
            "liability",
            "termination",
            "payment",
            "non_compete",
            "indemnification",
            "governing_law",
            "dispute_resolution",
            "force_majeure",
            "assignment",
            "amendment"
        ]
    )

@router.get("/contract/{contract_id}/analysis")
async def get_contract_analysis(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """Get analysis results for a specific contract"""
    try:
        analyzer_service = AnalyzerService(db)
        analysis = analyzer_service.get_contract_analysis(contract_id)
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found for this contract"
            )
        
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve analysis: {str(e)}"
        )
