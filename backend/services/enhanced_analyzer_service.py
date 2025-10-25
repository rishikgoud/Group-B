"""
Enhanced Contract Analysis Service
Industry-standard contract analysis with comprehensive processing pipeline
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import asyncio
import json
from pathlib import Path

from services.gemini_service import GeminiService
from services.file_processing_service import FileProcessingService
from services.contract_service import ContractService

logger = logging.getLogger(__name__)

class EnhancedAnalyzerService:
    """Industry-standard contract analysis service"""

    def __init__(self, db):
        self.db = db
        self.gemini_service = GeminiService()
        self.file_processor = FileProcessingService()
        self.contract_service = ContractService(db)

        # Analysis pipeline steps
        self.analysis_steps = [
            "file_validation",
            "text_extraction",
            "text_preprocessing",
            "document_classification",
            "clause_extraction",
            "risk_assessment",
            "compliance_checking",
            "final_validation"
        ]

    async def analyze_contract_comprehensive(
        self,
        contract_id: str,
        analysis_type: str = "standard",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive contract analysis following industry best practices

        Args:
            contract_id: ID of the contract to analyze
            analysis_type: Type of analysis (quick, standard, comprehensive)
            user_id: ID of the user requesting analysis

        Returns:
            Complete analysis results with metadata
        """

        start_time = datetime.utcnow()
        session_id = f"analysis_{contract_id}_{int(start_time.timestamp())}"

        logger.info(f"Starting comprehensive analysis for contract {contract_id}")

        try:
            # Step 1: Validate and get contract
            contract = await self.contract_service.get_contract_by_id(contract_id)
            if not contract:
                raise ValueError(f"Contract {contract_id} not found")

            # Step 2: Check if already analyzed
            if contract.processed and hasattr(contract, 'extracted_text'):
                logger.info(f"Contract {contract_id} already processed, using cached text")
                extracted_text = contract.extracted_text
            else:
                # Step 3: Extract text from file
                extraction_result = await self._extract_and_process_text(contract)
                extracted_text = extraction_result["text"]
                await self.contract_service.mark_contract_processed(contract_id, extracted_text)

            # Step 4: Preprocess text for better analysis
            processed_text = await self.file_processor.preprocess_text(extracted_text)

            # Step 5: Classify document type
            document_classification = await self._classify_document(processed_text)

            # Step 6: Perform comprehensive AI analysis
            analysis_result = await self.gemini_service.analyze_contract(processed_text)

            # Step 7: Validate and enhance results
            validated_result = await self._validate_and_enhance_analysis(
                analysis_result,
                processed_text,
                document_classification
            )

            # Step 8: Calculate processing time and metrics
            end_time = datetime.utcnow()
            processing_time = (end_time - start_time).total_seconds()

            # Step 9: Store analysis results
            analysis_data = {
                "contract_id": contract_id,
                "analysis_type": analysis_type,
                "overall_risk_score": validated_result.get("overall_risk_score", 5.0),
                "total_clauses": len(validated_result.get("clauses", [])),
                "risk_summary": validated_result.get("risk_summary", {}),
                "clauses": validated_result.get("clauses", []),
                "key_insights": validated_result.get("key_insights", []),
                "recommendations": validated_result.get("recommendations", []),
                "document_classification": document_classification,
                "analysis_metadata": {
                    "session_id": session_id,
                    "processing_time_seconds": processing_time,
                    "text_quality_score": self._calculate_text_quality(extracted_text),
                    "analysis_completeness": self._calculate_completeness(validated_result),
                    "ai_model_used": "gemini-pro",
                    "analysis_version": "2.0"
                },
                "analysis_date": end_time,
                "status": "completed"
            }

            # Step 10: Return comprehensive results
            return self._format_analysis_response(analysis_data)

        except Exception as e:
            logger.error(f"Comprehensive analysis failed for contract {contract_id}: {e}")
            raise Exception(f"Contract analysis failed: {str(e)}")

    async def _extract_and_process_text(self, contract) -> Dict[str, Any]:
        """Extract and process text with comprehensive validation"""

        logger.info(f"Extracting text from contract {contract.id}")

        # Validate file before processing
        validation_result = self.file_processor.validate_file(
            contract.file_path,
            contract.file_type
        )

        if not validation_result["valid"]:
            raise ValueError(f"File validation failed: {validation_result['errors']}")

        # Extract text
        extraction_result = await self.file_processor.extract_text_from_file(
            contract.file_path,
            contract.file_type
        )

        if not extraction_result["success"]:
            raise ValueError("Text extraction failed")

        return extraction_result

    async def _classify_document(self, text: str) -> Dict[str, Any]:
        """Classify document type and extract metadata"""

        try:
            # Simple rule-based classification (can be enhanced with ML)
            text_lower = text.lower()

            classifications = {
                "document_type": "contract",
                "industry": "general",
                "jurisdiction": "unknown"
            }

            # Industry classification
            if any(keyword in text_lower for keyword in ["employment", "employee", "employer", "salary", "wage"]):
                classifications["industry"] = "human_resources"
                classifications["document_type"] = "employment_contract"
            elif any(keyword in text_lower for keyword in ["lease", "rent", "tenant", "landlord", "property"]):
                classifications["industry"] = "real_estate"
                classifications["document_type"] = "lease_agreement"
            elif any(keyword in text_lower for keyword in ["nda", "confidential", "non-disclosure"]):
                classifications["document_type"] = "nda"
            elif any(keyword in text_lower for keyword in ["vendor", "supplier", "purchase", "procurement"]):
                classifications["industry"] = "procurement"
                classifications["document_type"] = "vendor_agreement"

            # Jurisdiction detection (basic)
            if any(keyword in text_lower for keyword in ["california", "ca", "new york", "ny", "texas", "tx"]):
                classifications["jurisdiction"] = "usa"

            return classifications

        except Exception as e:
            logger.error(f"Document classification failed: {e}")
            return {"document_type": "contract", "industry": "general", "jurisdiction": "unknown"}

    async def _validate_and_enhance_analysis(
        self,
        analysis_result: Dict[str, Any],
        original_text: str,
        document_classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate and enhance AI analysis results"""

        # Validate analysis structure
        if not analysis_result.get("clauses"):
            analysis_result["clauses"] = []

        # Enhance clause analysis with document context
        for clause in analysis_result["clauses"]:
            # Add document classification context
            clause["document_context"] = document_classification

            # Validate risk scores are within bounds
            if "risk_score" in clause:
                clause["risk_score"] = max(0, min(10, float(clause["risk_score"])))

            # Ensure recommendations are actionable
            if "recommendations" in clause and isinstance(clause["recommendations"], list):
                clause["recommendations"] = [
                    rec for rec in clause["recommendations"]
                    if len(rec.strip()) > 10  # Filter out very short recommendations
                ]

        # Add overall analysis enhancements
        analysis_result["document_classification"] = document_classification
        analysis_result["text_length"] = len(original_text)
        analysis_result["analysis_confidence"] = self._calculate_confidence(analysis_result)

        # Recalculate risk summary if needed
        if analysis_result["clauses"]:
            risk_summary = {"high": 0, "medium": 0, "low": 0}
            for clause in analysis_result["clauses"]:
                risk_level = clause.get("risk_level", "low").lower()
                if risk_level in risk_summary:
                    risk_summary[risk_level] += 1

            analysis_result["risk_summary"] = risk_summary

        return analysis_result

    def _calculate_text_quality(self, text: str) -> float:
        """Calculate text extraction quality score (0-1)"""

        if not text:
            return 0.0

        score = 1.0

        # Check for common OCR issues
        ocr_artifacts = text.count('|') + text.count('_') + text.count('*')
        score -= min(0.3, ocr_artifacts / len(text) * 10)

        # Check text coherence
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if len(sentences) < 3:
            score -= 0.2

        # Check for reasonable length
        if len(text) < 100:
            score -= 0.3
        elif len(text) > 50000:  # Very long documents
            score -= 0.1

        return max(0.0, min(1.0, score))

    def _calculate_confidence(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate overall analysis confidence score"""

        base_score = 0.8  # Start with good confidence

        # Adjust based on number of clauses found
        clauses_count = len(analysis_result.get("clauses", []))
        if clauses_count == 0:
            base_score -= 0.3
        elif clauses_count < 3:
            base_score -= 0.1

        # Adjust based on risk score distribution
        risk_summary = analysis_result.get("risk_summary", {})
        total_clauses = sum(risk_summary.values())
        if total_clauses > 0:
            # Penalize if all clauses have same risk level (might indicate poor analysis)
            if max(risk_summary.values()) == total_clauses:
                base_score -= 0.1

        return max(0.0, min(1.0, base_score))

    def _calculate_completeness(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate analysis completeness score"""

        completeness = 0.0
        checks = 0

        # Check for required fields
        required_fields = ["clauses", "overall_risk_score", "key_insights", "risk_summary"]
        for field in required_fields:
            checks += 1
            if field in analysis_result and analysis_result[field]:
                completeness += 1.0 / len(required_fields)

        # Check clause quality
        if analysis_result.get("clauses"):
            for clause in analysis_result["clauses"]:
                clause_completeness = 0
                clause_checks = ["clause_text", "clause_type", "risk_level", "simplified_explanation"]
                for check in clause_checks:
                    if check in clause and clause[check]:
                        clause_completeness += 0.25
                completeness += clause_completeness * 0.1  # Weight clause completeness

        return min(1.0, completeness)

    def _format_analysis_response(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format analysis response in frontend-compatible format"""

        return {
            "analysis_id": analysis_data["analysis_metadata"]["session_id"],
            "contract_id": analysis_data["contract_id"],
            "total_clauses": analysis_data["total_clauses"],
            "risk_summary": analysis_data["risk_summary"],
            "overall_risk_score": analysis_data["overall_risk_score"],
            "key_insights": analysis_data["key_insights"],
            "document_classification": analysis_data["document_classification"],
            "analysis_metadata": analysis_data["analysis_metadata"],
            "clauses": analysis_data["clauses"],
            "analysis_date": analysis_data["analysis_date"],
            "processing_time": analysis_data["analysis_metadata"]["processing_time_seconds"]
        }
