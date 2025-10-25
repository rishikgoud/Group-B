"""
Enhanced contract analyzer service with Gemini AI integration
"""

from app.models.mongodb_models import Contract, ContractAnalysis, ContractClause
from app.models.schemas import ClauseAnalysis
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging

from services.advanced_gemini_service import AdvancedGeminiDocumentService
from services.file_processing_service import FileProcessingService

logger = logging.getLogger(__name__)

class AnalyzerService:
    def __init__(self, db):
        self.db = db
        self.advanced_gemini_service = AdvancedGeminiDocumentService()
        self.file_processor = FileProcessingService()
    
    async def analyze_contract(self, contract_id: str, analysis_type: str = "full") -> Dict[str, Any]:
        """Analyze a contract using AI"""
        
        # Get contract
        contract = await Contract.get(contract_id)
        if not contract:
            raise ValueError("Contract not found")
        
        try:
            # Extract text from file if not already processed
            if not contract.processed or not contract.extracted_text:
                logger.info(f"Extracting text from contract {contract_id}")
                extraction_result = await self.file_processor.extract_text_from_file(
                    contract.file_path, 
                    contract.file_type
                )
                
                if not extraction_result["success"]:
                    raise Exception("Failed to extract text from contract")
                
                # Update contract with extracted text
                contract.extracted_text = extraction_result["text"]
                contract.processed = True
                await contract.save()

            # Analyze with advanced Gemini AI using native PDF processing
            logger.info(f"Analyzing contract {contract_id} with advanced Gemini AI")

            # Determine processing method based on file type
            if contract.file_type.lower() == 'pdf':
                # Use native PDF processing for PDFs
                analysis_result = await self.advanced_gemini_service.process_contract_document(
                    file_path=contract.file_path,
                    processing_type="comprehensive"
                )
            else:
                # Use text processing for other formats
                analysis_result = await self.advanced_gemini_service.process_contract_document(
                    contract_text=contract.extracted_text,
                    processing_type="comprehensive"
                )
            
            # Create analysis record
            analysis = ContractAnalysis(
                contract_id=contract_id,
                analysis_type=analysis_type,
                overall_risk_score=analysis_result.get("risk_analysis", {}).get("overall_risk_score", 5.0),
                total_clauses=len(analysis_result.get("clauses", [])),
                high_risk_clauses=analysis_result.get("risk_analysis", {}).get("risk_distribution", {}).get("high", 0),
                medium_risk_clauses=analysis_result.get("risk_analysis", {}).get("risk_distribution", {}).get("medium", 0),
                low_risk_clauses=analysis_result.get("risk_analysis", {}).get("risk_distribution", {}).get("low", 0),
                analysis_date=datetime.utcnow(),
                ai_model_used="gemini-1.5-flash"
            )
            
            await analysis.insert()
            
            # Create clause records
            clauses_data = []
            for clause_data in analysis_result.get("clauses", []):
                clause = ContractClause(
                    contract_id=contract_id,
                    clause_text=clause_data["clause_text"],
                    clause_type=clause_data["clause_type"],
                    risk_level=clause_data["risk_level"],
                    risk_score=clause_data["risk_score"],
                    simplified_explanation=clause_data["simplified_explanation"],
                    recommendations=clause_data["recommendations"] if clause_data["recommendations"] else [],
                    start_position=clause_data.get("start_position", 0),
                    end_position=clause_data.get("end_position", 0)
                )
                await clause.insert()
                clauses_data.append(clause)
            
            # Convert clauses to response format
            clause_responses = []
            for clause in clauses_data:
                clause_responses.append(ClauseAnalysis(
                    clause_text=clause.clause_text,
                    clause_type=clause.clause_type,
                    risk_level=clause.risk_level,
                    risk_score=clause.risk_score,
                    simplified_explanation=clause.simplified_explanation,
                    recommendations=clause.recommendations,
                    start_position=clause.start_position,
                    end_position=clause.end_position
                ))
            
            return {
                "analysis_id": analysis.id,
                "contract_id": contract_id,
                "total_clauses": analysis.total_clauses,
                "risk_summary": {
                    "high": analysis.high_risk_clauses,
                    "medium": analysis.medium_risk_clauses,
                    "low": analysis.low_risk_clauses
                },
                "overall_risk_score": analysis.overall_risk_score,
                "key_insights": analysis_result.get("key_insights", []),
                "recommendations": analysis_result.get("recommendations", []),
                "document_classification": analysis_result.get("document_overview", {}),
                "compliance_analysis": analysis_result.get("compliance_analysis", {}),
                "structural_analysis": analysis_result.get("structural_analysis", {}),
                "analysis_metadata": analysis_result.get("analysis_metadata", {}),
                "clauses": clause_responses,
                "analysis_date": analysis.analysis_date
            }
            
        except Exception as e:
            logger.error(f"Error analyzing contract {contract_id}: {e}")
            raise Exception(f"Contract analysis failed: {str(e)}")
    
    async def explain_clause(self, clause_text: str, clause_type: str) -> Dict[str, Any]:
        """Get detailed explanation for a specific clause"""
        
        try:
            explanation = await self.advanced_gemini_service.explain_clause_enhanced(
                clause_text, clause_type
            )
            return explanation
        except Exception as e:
            logger.error(f"Error explaining clause: {e}")
            return {
                "plain_english": "Unable to generate explanation",
                "business_purpose": "Explanation failed",
                "risks_concerns": [],
                "market_standard": "unknown",
                "negotiation_tips": [],
                "compliance_notes": [],
                "real_examples": [],
                "confidence_level": "low"
            }
    
    async def compare_clauses(self, clause1: str, clause2: str) -> Dict[str, Any]:
        """Compare two clauses and highlight differences"""
        
        try:
            comparison = await self.advanced_gemini_service.compare_contracts(
                clause1, clause2, "detailed"
            )
            return comparison
        except Exception as e:
            logger.error(f"Error comparing clauses: {e}")
            return {
                "comparison_summary": "Comparison failed",
                "clause_differences": [],
                "risk_analysis": {},
                "financial_impact": {},
                "recommendations": ["Review clauses manually"]
            }
    
    async def get_contract_analysis(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Get analysis results for a contract"""
        analysis = await ContractAnalysis.find(
            ContractAnalysis.contract_id == contract_id
        ).sort(-ContractAnalysis.analysis_date).first()
        
        if not analysis:
            return None
        
        # Get clauses
        clauses = await ContractClause.find(
            ContractClause.contract_id == contract_id
        ).to_list()
        
        clause_data = []
        for clause in clauses:
            clause_data.append({
                "clause_text": clause.clause_text,
                "clause_type": clause.clause_type,
                "risk_level": clause.risk_level,
                "risk_score": clause.risk_score,
                "simplified_explanation": clause.simplified_explanation,
                "recommendations": clause.recommendations
            })
        
        return {
            "analysis_id": str(analysis.id),
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
