"""
Contract analyzer service for AI-powered analysis
"""

from sqlalchemy.orm import Session
from app.models.database import Contract, ContractAnalysis, ContractClause
from app.models.schemas import ClauseAnalysis
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class AnalyzerService:
    def __init__(self, db: Session):
        self.db = db
    
    async def analyze_contract(self, contract_id: int, analysis_type: str = "full") -> Dict[str, Any]:
        """Analyze a contract using AI"""
        
        # Get contract
        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise ValueError("Contract not found")
        
        # TODO: Implement actual AI analysis
        # For now, return mock analysis
        mock_analysis = self._generate_mock_analysis(contract_id)
        
        # Create analysis record
        analysis = ContractAnalysis(
            contract_id=contract_id,
            analysis_type=analysis_type,
            overall_risk_score=mock_analysis["overall_risk_score"],
            total_clauses=mock_analysis["total_clauses"],
            high_risk_clauses=mock_analysis["risk_summary"]["high"],
            medium_risk_clauses=mock_analysis["risk_summary"]["medium"],
            low_risk_clauses=mock_analysis["risk_summary"]["low"],
            analysis_date=datetime.utcnow(),
            ai_model_used="mock_model"
        )
        
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        
        # Create clause records
        for clause_data in mock_analysis["clauses"]:
            clause = ContractClause(
                contract_id=contract_id,
                clause_text=clause_data.clause_text,
                clause_type=clause_data.clause_type,
                risk_level=clause_data.risk_level,
                risk_score=clause_data.risk_score,
                simplified_explanation=clause_data.simplified_explanation,
                recommendations=json.dumps(clause_data.recommendations) if clause_data.recommendations else None
            )
            self.db.add(clause)
        
        self.db.commit()
        
        return {
            "analysis_id": analysis.id,
            "total_clauses": mock_analysis["total_clauses"],
            "risk_summary": mock_analysis["risk_summary"],
            "clauses": mock_analysis["clauses"],
            "overall_risk_score": mock_analysis["overall_risk_score"],
            "key_insights": mock_analysis["key_insights"],
            "analysis_date": analysis.analysis_date
        }
    
    def _generate_mock_analysis(self, contract_id: int) -> Dict[str, Any]:
        """Generate mock analysis data"""
        return {
            "total_clauses": 15,
            "risk_summary": {"high": 2, "medium": 5, "low": 8},
            "clauses": [
                ClauseAnalysis(
                    clause_text="The Company shall maintain strict confidentiality regarding all proprietary information...",
                    clause_type="confidentiality",
                    risk_level="medium",
                    risk_score=6.5,
                    simplified_explanation="You must keep company information secret",
                    recommendations=["Review what information is considered confidential", "Understand the duration of confidentiality"]
                ),
                ClauseAnalysis(
                    clause_text="Employee agrees to assign all intellectual property rights to the Company...",
                    clause_type="intellectual_property",
                    risk_level="high",
                    risk_score=8.5,
                    simplified_explanation="The company owns all your work and ideas",
                    recommendations=["Negotiate carve-outs for personal projects", "Understand scope of IP assignment"]
                ),
                ClauseAnalysis(
                    clause_text="This agreement shall be governed by the laws of the State of California...",
                    clause_type="governing_law",
                    risk_level="low",
                    risk_score=2.0,
                    simplified_explanation="California law applies to this contract",
                    recommendations=["Understand local legal implications"]
                )
            ],
            "overall_risk_score": 6.5,
            "key_insights": [
                "Strong IP assignment clause may limit personal projects",
                "Confidentiality obligations extend beyond employment",
                "Consider negotiating termination conditions"
            ]
        }
    
    def get_contract_analysis(self, contract_id: int) -> Optional[Dict[str, Any]]:
        """Get analysis results for a contract"""
        analysis = self.db.query(ContractAnalysis).filter(
            ContractAnalysis.contract_id == contract_id
        ).order_by(ContractAnalysis.analysis_date.desc()).first()
        
        if not analysis:
            return None
        
        # Get clauses
        clauses = self.db.query(ContractClause).filter(
            ContractClause.contract_id == contract_id
        ).all()
        
        clause_data = []
        for clause in clauses:
            recommendations = []
            if clause.recommendations:
                try:
                    recommendations = json.loads(clause.recommendations)
                except json.JSONDecodeError:
                    recommendations = [clause.recommendations]
            
            clause_data.append({
                "clause_text": clause.clause_text,
                "clause_type": clause.clause_type,
                "risk_level": clause.risk_level,
                "risk_score": clause.risk_score,
                "simplified_explanation": clause.simplified_explanation,
                "recommendations": recommendations
            })
        
        return {
            "analysis_id": analysis.id,
            "contract_id": contract_id,
            "analysis_type": analysis.analysis_type,
            "overall_risk_score": analysis.overall_risk_score,
            "total_clauses": analysis.total_clauses,
            "risk_summary": {
                "high": analysis.high_risk_clauses,
                "medium": analysis.medium_risk_clauses,
                "low": analysis.low_risk_clauses
            },
            "clauses": clause_data,
            "analysis_date": analysis.analysis_date,
            "ai_model_used": analysis.ai_model_used
        }
