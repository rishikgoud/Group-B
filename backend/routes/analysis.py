"""
Contract analysis routes
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.models.mongodb_models import Contract, ContractAnalysis, ContractClause
from app.models.schemas import (
    AnalysisRequest, 
    ContractAnalysisResponse, 
    RiskLevelsResponse, 
    ClauseTypesResponse
)
from services.advanced_gemini_service import AdvancedGeminiDocumentService

router = APIRouter()

@router.post("/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(
    request: AnalysisRequest,
    db = Depends(get_database)
):
    """Analyze a contract and extract insights"""
    try:
        analyzer_service = EnhancedAnalyzerService(db)
        result = await analyzer_service.analyze_contract_comprehensive(
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
            message="Contract analysis completed successfully",
            metadata=result.get("analysis_metadata", {}),
            document_classification=result.get("document_classification", {})
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze contract: {str(e)}"
        )

@router.post("/explain-clause")
async def explain_clause(
    clause_text: str,
    clause_type: str,
    db = Depends(get_database)
):
    """Get detailed explanation for a specific clause"""
    
    try:
        analyzer = AnalyzerService(db)
        explanation = await analyzer.explain_clause(clause_text, clause_type)
        
        return explanation
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to explain clause: {str(e)}"
        )

@router.post("/compare-clauses")
async def compare_clauses(
    clause1_text: str,
    clause2_text: str,
    db = Depends(get_database)
):
    """Compare two clauses and highlight differences"""
    
    try:
        analyzer = AnalyzerService(db)
        comparison = await analyzer.compare_clauses(clause1_text, clause2_text)
        
        return comparison
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compare clauses: {str(e)}"
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
    contract_id: str,
    db = Depends(get_database)
):
    """Get analysis results for a specific contract"""
    try:
        analyzer_service = AnalyzerService(db)
        analysis = await analyzer_service.get_contract_analysis(contract_id)
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found for this contract"
            )
        
@router.post("/chat")
async def chat_with_contract(
    contract_text: str,
    question: str,
    contract_context: Optional[Dict[str, Any]] = None,
    db = Depends(get_database)
):
    """Chat with contract using contextual AI"""
    try:
        advanced_gemini = AdvancedGeminiDocumentService()
        response = await advanced_gemini.chat_with_contract(
            contract_text, question, contract_context
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat request: {str(e)}"
        )

@router.post("/compare-contracts")
async def compare_contracts(
    contract1_id: str,
    contract2_id: str,
    comparison_type: str = "comprehensive",
    db = Depends(get_database)
):
    """Compare two contracts and highlight differences"""
    try:
        # Get both contracts
        contract1 = await Contract.get(contract1_id)
        contract2 = await Contract.get(contract2_id)

        if not contract1 or not contract2:
            raise HTTPException(
                status_code=404,
                detail="One or both contracts not found"
            )

        # Extract text from both contracts
        contract1_text = contract1.extracted_text if contract1.processed else ""
        contract2_text = contract2.extracted_text if contract2.processed else ""

        if not contract1_text or not contract2_text:
            raise HTTPException(
                status_code=400,
                detail="Both contracts must be processed before comparison"
            )

        # Use advanced comparison
        advanced_gemini = AdvancedGeminiDocumentService()
        comparison = await advanced_gemini.compare_contracts(
            contract1_text, contract2_text, comparison_type
        )

        return comparison

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compare contracts: {str(e)}"
        )

@router.post("/extract-structured-data")
async def extract_structured_data(
    contract_id: str,
    data_types: List[str] = None,
    db = Depends(get_database)
):
    """Extract structured data from contract"""
    try:
        if data_types is None:
            data_types = ["financial", "dates", "parties", "obligations"]

        # Get contract
        contract = await Contract.get(contract_id)
        if not contract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )

        if not contract.processed or not contract.extracted_text:
            raise HTTPException(
                status_code=400,
                detail="Contract must be processed before data extraction"
            )

        # Use advanced extraction
        advanced_gemini = AdvancedGeminiDocumentService()
        extraction_result = await advanced_gemini.extract_structured_data({
            "data": contract.extracted_text,
            "format": "txt",
            "filename": contract.file_name,
            "size": len(contract.extracted_text)
        }, data_types)

        return extraction_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract structured data: {str(e)}"
        )

@router.get("/analytics/dashboard")
async def get_analytics_dashboard(db = Depends(get_database)):
    """Generate analytics dashboard for all contracts"""
    try:
        # Get all analyses
        analyses = await ContractAnalysis.find().to_list()

        if not analyses:
            return {
                "dashboard_data": {
                    "total_contracts": 0,
                    "risk_distribution": {"critical": 0, "high": 0, "medium": 0, "low": 0},
                    "top_clause_types": {},
                    "average_risk_score": 0,
                    "risk_trend": "stable"
                },
                "insights": ["No contracts analyzed yet"],
                "recommendations": ["Upload and analyze some contracts to see analytics"]
            }

        # Get detailed analysis data
        contracts_data = []
        for analysis in analyses:
            clauses = await ContractClause.find(
                ContractClause.contract_id == analysis.contract_id
            ).to_list()

            contract_data = {
                "contract_id": analysis.contract_id,
                "analysis_type": analysis.analysis_type,
                "overall_risk_score": analysis.overall_risk_score,
                "total_clauses": analysis.total_clauses,
                "risk_summary": {
                    "high": analysis.high_risk_clauses,
                    "medium": analysis.medium_risk_clauses,
                    "low": analysis.low_risk_clauses
                },
                "clauses": [
                    {
                        "clause_type": clause.clause_type,
                        "risk_level": clause.risk_level,
                        "risk_score": clause.risk_score
                    }
                    for clause in clauses
                ],
                "analysis_date": analysis.analysis_date
            }
            contracts_data.append(contract_data)

        # Generate analytics using advanced service
        advanced_gemini = AdvancedGeminiDocumentService()
        analytics = await advanced_gemini.generate_analytics_dashboard(
            contracts_data, "comprehensive"
        )

        return analytics

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate analytics: {str(e)}"
        )
