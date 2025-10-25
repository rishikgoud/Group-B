"""
Contract analysis endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel

router = APIRouter()

class AnalysisRequest(BaseModel):
    """Request model for contract analysis"""
    contract_id: str
    analysis_type: str = "full"  # full, risk_only, clause_extraction

class ClauseAnalysis(BaseModel):
    """Model for clause analysis result"""
    clause_text: str
    clause_type: str
    risk_level: str  # high, medium, low
    simplified_explanation: str
    recommendations: List[str]

class ContractAnalysis(BaseModel):
    """Model for complete contract analysis"""
    contract_id: str
    total_clauses: int
    risk_summary: Dict[str, int]  # {"high": 2, "medium": 5, "low": 8}
    clauses: List[ClauseAnalysis]
    overall_risk_score: float
    key_insights: List[str]

@router.post("/analyze", response_model=ContractAnalysis)
async def analyze_contract(request: AnalysisRequest):
    """Analyze a contract and extract insights"""
    
    # TODO: Implement actual AI analysis
    # This is a placeholder response
    
    mock_analysis = ContractAnalysis(
        contract_id=request.contract_id,
        total_clauses=15,
        risk_summary={"high": 2, "medium": 5, "low": 8},
        clauses=[
            ClauseAnalysis(
                clause_text="The Company shall maintain strict confidentiality...",
                clause_type="confidentiality",
                risk_level="medium",
                simplified_explanation="You must keep company information secret",
                recommendations=["Review what information is considered confidential", "Understand the duration of confidentiality"]
            ),
            ClauseAnalysis(
                clause_text="Employee agrees to assign all intellectual property...",
                clause_type="intellectual_property",
                risk_level="high",
                simplified_explanation="The company owns all your work and ideas",
                recommendations=["Negotiate carve-outs for personal projects", "Understand scope of IP assignment"]
            )
        ],
        overall_risk_score=6.5,
        key_insights=[
            "Strong IP assignment clause may limit personal projects",
            "Confidentiality obligations extend beyond employment",
            "Consider negotiating termination conditions"
        ]
    )
    
    return mock_analysis

@router.get("/risk-levels")
async def get_risk_levels():
    """Get available risk levels and their descriptions"""
    return {
        "risk_levels": {
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
    }

@router.get("/clause-types")
async def get_clause_types():
    """Get available clause types for classification"""
    return {
        "clause_types": [
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
    }
