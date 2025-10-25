"""
Advanced Gemini Document Processing Service
Leverages Gemini's native PDF understanding capabilities for comprehensive contract analysis
"""

import google.generativeai as genai
from google.generativeai import types
from typing import List, Dict, Any, Optional, Union
import json
import logging
import os
import asyncio
from pathlib import Path
from datetime import datetime
import time
import httpx
import io
from urllib.parse import urlparse
from app.core.config import settings

logger = logging.getLogger(__name__)

class AdvancedGeminiDocumentService:
    """
    Advanced document processing service using Gemini's native PDF capabilities

    Features:
    - Native PDF processing with vision understanding
    - Large document support (up to 1000 pages)
    - Structured data extraction
    - Multi-document comparison
    - Layout and formatting preservation
    - Visual element analysis (charts, diagrams, tables)
    """

    def __init__(self):
        """Initialize advanced Gemini document service"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use Gemini 1.5 Flash for document processing
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # File API client for large documents
        self.file_client = genai.Client()

        # Document processing limits
        self.max_pages = 1000
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.supported_mime_types = [
            'application/pdf',
            'text/plain',
            'text/markdown',
            'text/html',
            'application/xml'
        ]

    async def process_contract_document(
        self,
        file_path: Optional[str] = None,
        file_url: Optional[str] = None,
        contract_text: Optional[str] = None,
        processing_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Process contract document using Gemini's advanced capabilities

        Args:
            file_path: Local file path (for files under 20MB)
            file_url: URL to download file from
            contract_text: Raw contract text (fallback)
            processing_type: Type of processing (quick, comprehensive, structured)

        Returns:
            Comprehensive analysis with structured data
        """

        start_time = time.time()

        try:
            logger.info(f"Starting advanced document processing (type: {processing_type})")

            # Get document content
            if file_path:
                document_data = await self._load_local_file(file_path)
            elif file_url:
                document_data = await self._load_file_from_url(file_url)
            elif contract_text:
                document_data = {"text": contract_text, "format": "text"}
            else:
                raise ValueError("No document source provided")

            # Process based on document format and size
            if document_data["format"] == "pdf":
                if document_data["size"] > 20 * 1024 * 1024:  # 20MB
                    result = await self._process_large_pdf(document_data, processing_type)
                else:
                    result = await self._process_pdf_with_vision(document_data, processing_type)
            else:
                result = await self._process_text_document(document_data, processing_type)

            # Add processing metadata
            processing_time = time.time() - start_time
            result["processing_metadata"] = {
                "processing_time_seconds": processing_time,
                "document_format": document_data["format"],
                "document_size": document_data["size"],
                "processing_type": processing_type,
                "ai_model_used": "gemini-1.5-flash",
                "api_version": "v1beta"
            }

            logger.info(f"Advanced document processing completed in {processing_time:.2f".2f"conds")
            return result

        except Exception as e:
            logger.error(f"Advanced document processing failed: {e}")
            raise Exception(f"Document processing failed: {str(e)}")

    async def _load_local_file(self, file_path: str) -> Dict[str, Any]:
        """Load and validate local file"""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size:
            raise ValueError(f"File too large: {file_size} bytes (max: {self.max_file_size})")

        # Determine MIME type
        file_extension = Path(file_path).suffix.lower()
        mime_type = self._get_mime_type(file_extension)

        return {
            "data": Path(file_path).read_bytes(),
            "format": file_extension[1:],  # Remove dot
            "mime_type": mime_type,
            "size": file_size,
            "filename": Path(file_path).name
        }

    async def _load_file_from_url(self, url: str) -> Dict[str, Any]:
        """Load file from URL"""

        try:
            # Download file
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()

                content = response.content
                content_length = len(content)

                if content_length > self.max_file_size:
                    raise ValueError(f"Downloaded file too large: {content_length} bytes")

                # Determine format from URL or content
                parsed_url = urlparse(url)
                file_extension = Path(parsed_url.path).suffix.lower()
                mime_type = self._get_mime_type(file_extension)

                return {
                    "data": content,
                    "format": file_extension[1:] if file_extension else "pdf",
                    "mime_type": mime_type,
                    "size": content_length,
                    "url": url
                }

        except httpx.RequestError as e:
            raise Exception(f"Failed to download file from URL: {e}")

    def _get_mime_type(self, file_extension: str) -> str:
        """Get MIME type from file extension"""

        mime_types = {
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.html': 'text/html',
            '.xml': 'application/xml',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }

        return mime_types.get(file_extension.lower(), 'application/pdf')

    async def _process_pdf_with_vision(
        self,
        document_data: Dict[str, Any],
        processing_type: str
    ) -> Dict[str, Any]:
        """Process PDF using Gemini's vision capabilities"""

        try:
            # Create processing prompt based on type
            prompt = self._create_document_analysis_prompt(processing_type)

            # Process with Gemini's native PDF understanding
            response = self.model.generate_content([
                types.Part.from_bytes(
                    data=document_data["data"],
                    mime_type=document_data["mime_type"]
                ),
                prompt
            ])

            # Parse structured response
            result = self._parse_structured_response(response.text, processing_type)

            # Add document metadata
            result["document_metadata"] = {
                "filename": document_data["filename"],
                "file_size": document_data["size"],
                "mime_type": document_data["mime_type"],
                "processing_method": "gemini_vision"
            }

            return result

        except Exception as e:
            logger.error(f"Vision PDF processing failed: {e}")
            # Fallback to text extraction
            return await self._fallback_text_processing(document_data, processing_type)

    async def _process_large_pdf(
        self,
        document_data: Dict[str, Any],
        processing_type: str
    ) -> Dict[str, Any]:
        """Process large PDF using File API"""

        try:
            logger.info(f"Processing large PDF ({document_data['size']} bytes) with File API")

            # Upload to File API
            doc_io = io.BytesIO(document_data["data"])
            uploaded_file = self.file_client.files.upload(
                file=doc_io,
                config=dict(mime_type=document_data["mime_type"])
            )

            # Create processing prompt
            prompt = self._create_document_analysis_prompt(processing_type)

            # Process with uploaded file
            response = self.model.generate_content([
                uploaded_file,
                prompt
            ])

            # Parse response
            result = self._parse_structured_response(response.text, processing_type)

            # Add metadata
            result["document_metadata"] = {
                "filename": document_data["filename"],
                "file_size": document_data["size"],
                "mime_type": document_data["mime_type"],
                "processing_method": "file_api",
                "uploaded_file_id": uploaded_file.name
            }

            return result

        except Exception as e:
            logger.error(f"File API processing failed: {e}")
            raise Exception(f"Large PDF processing failed: {str(e)}")

    async def _process_text_document(
        self,
        document_data: Dict[str, Any],
        processing_type: str
    ) -> Dict[str, Any]:
        """Process text-based documents"""

        try:
            # Convert bytes to text if needed
            if isinstance(document_data["data"], bytes):
                text_content = document_data["data"].decode('utf-8')
            else:
                text_content = document_data["data"]

            # Create processing prompt
            prompt = self._create_document_analysis_prompt(processing_type)

            # Process with Gemini
            response = self.model.generate_content(f"{prompt}\n\nDOCUMENT TEXT:\n{text_content}")

            # Parse response
            result = self._parse_structured_response(response.text, processing_type)

            # Add metadata
            result["document_metadata"] = {
                "filename": document_data["filename"],
                "file_size": document_data["size"],
                "mime_type": document_data["mime_type"],
                "processing_method": "text_analysis"
            }

            return result

        except UnicodeDecodeError:
            raise Exception("Unable to decode document as text")
        except Exception as e:
            logger.error(f"Text document processing failed: {e}")
            raise Exception(f"Text processing failed: {str(e)}")

    async def _fallback_text_processing(
        self,
        document_data: Dict[str, Any],
        processing_type: str
    ) -> Dict[str, Any]:
        """Fallback processing using traditional text extraction"""

        logger.warning("Falling back to traditional text extraction")

        try:
            # Use existing file processing service
            from services.file_processing_service import FileProcessingService

            file_processor = FileProcessingService()
            extraction_result = await file_processor.extract_text_from_file(
                document_data["filepath"] if "filepath" in document_data else "temp_file",
                document_data["format"]
            )

            # Process extracted text
            return await self._process_text_document({
                "data": extraction_result["text"],
                "format": "txt",
                "filename": document_data["filename"],
                "size": len(extraction_result["text"])
            }, processing_type)

        except Exception as e:
            logger.error(f"Fallback processing failed: {e}")
            raise Exception(f"All processing methods failed: {str(e)}")

    def _create_document_analysis_prompt(self, processing_type: str) -> str:
        """Create comprehensive document analysis prompt"""

        if processing_type == "quick":
            return self._create_quick_analysis_prompt()
        elif processing_type == "comprehensive":
            return self._create_comprehensive_analysis_prompt()
        elif processing_type == "structured":
            return self._create_structured_analysis_prompt()
        else:
            return self._create_comprehensive_analysis_prompt()

    def _create_quick_analysis_prompt(self) -> str:
        """Quick analysis prompt for fast processing"""

        return """
Analyze this contract document and provide a quick overview:

1. Document type and industry
2. Key parties involved
3. Overall risk level (low/medium/high)
4. Top 3 most important clauses
5. Main concerns or red flags

Format as JSON:
{
    "document_type": "string",
    "industry": "string",
    "parties": ["party1", "party2"],
    "overall_risk": "low/medium/high",
    "key_clauses": ["clause1", "clause2", "clause3"],
    "main_concerns": ["concern1", "concern2"],
    "summary": "brief summary"
}
"""

    def _create_comprehensive_analysis_prompt(self) -> str:
        """Comprehensive analysis prompt for detailed processing"""

        return """
Perform comprehensive legal contract analysis using advanced document understanding:

1. DOCUMENT OVERVIEW
   - Document type (employment, NDA, lease, service agreement, etc.)
   - Industry sector and context
   - All parties and their roles
   - Contract duration and effective dates
   - Geographic jurisdiction

2. CLAUSE IDENTIFICATION & ANALYSIS
   Extract and analyze ALL clauses including:
   - Exact clause text from document
   - Clause classification (confidentiality, liability, payment, etc.)
   - Risk assessment (low/medium/high/critical)
   - Legal implications and concerns
   - Market standard comparison
   - Negotiation recommendations

3. STRUCTURAL ANALYSIS
   - Document organization and flow
   - Cross-references between sections
   - Consistency in terminology
   - Completeness of essential provisions
   - Layout and formatting quality

4. VISUAL ELEMENT ANALYSIS
   - Tables and their content
   - Charts or diagrams interpretation
   - Images and their relevance
   - Document layout insights

5. COMPLIANCE & REGULATORY
   - Regulatory framework requirements
   - Compliance obligations
   - Data protection considerations
   - Industry-specific regulations

6. FINANCIAL IMPACT
   - Payment terms and conditions
   - Financial exposure assessment
   - Liability limitations
   - Insurance requirements

Provide comprehensive analysis in this JSON format:
{
    "document_overview": {
        "document_type": "string",
        "industry": "string",
        "parties": ["party1", "party2"],
        "duration": "string",
        "jurisdiction": "string",
        "total_pages": "number",
        "word_count": "number"
    },
    "clauses": [
        {
            "clause_text": "exact text from document",
            "clause_type": "classification",
            "risk_level": "low/medium/high/critical",
            "risk_score": "number 0-10",
            "confidence": "number 0-1",
            "legal_implications": ["implication1", "implication2"],
            "market_standard": "above/below/at standard",
            "negotiation_points": ["point1", "point2"],
            "financial_impact": "low/medium/high",
            "compliance_requirements": ["req1", "req2"],
            "page_number": "number",
            "section": "string"
        }
    ],
    "risk_analysis": {
        "overall_risk_score": "number 0-10",
        "risk_distribution": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        "top_risks": ["risk1", "risk2", "risk3"],
        "financial_exposure": "low/medium/high/critical"
    },
    "key_insights": [
        "insight1",
        "insight2",
        "insight3"
    ],
    "recommendations": [
        "recommendation1",
        "recommendation2"
    ],
    "compliance_analysis": {
        "regulatory_framework": ["GDPR", "CCPA", "SOX"],
        "compliance_score": "number 0-10",
        "compliance_issues": ["issue1", "issue2"],
        "required_actions": ["action1", "action2"]
    },
    "structural_analysis": {
        "document_quality_score": "number 0-10",
        "completeness_score": "number 0-10",
        "clarity_score": "number 0-10",
        "consistency_score": "number 0-10",
        "visual_elements": ["table1", "chart1", "diagram1"]
    }
}
"""

    def _create_structured_analysis_prompt(self) -> str:
        """Structured analysis prompt for data extraction"""

        return """
Extract structured data from this contract document. Focus on creating clean, organized data suitable for database storage and further processing:

1. EXTRACT ALL STRUCTURED INFORMATION:
   - Contract metadata (title, date, parties, etc.)
   - All clauses with their types and content
   - Financial terms and amounts
   - Dates and deadlines
   - Compliance requirements
   - Contact information
   - Geographic locations

2. IDENTIFY VISUAL ELEMENTS:
   - Tables and their structured data
   - Charts and their values
   - Diagrams and their meaning
   - Signatures and approvals

3. CLASSIFY AND CATEGORIZE:
   - Document sections and their purposes
   - Clause categories and relationships
   - Risk levels and priorities
   - Action items and requirements

Format as structured JSON with clear data organization:
{
    "contract_metadata": {
        "title": "string",
        "execution_date": "date",
        "effective_date": "date",
        "expiration_date": "date",
        "parties": [
            {"name": "string", "role": "string", "type": "individual/corporation"}
        ],
        "jurisdiction": "string",
        "governing_law": "string"
    },
    "structured_clauses": [
        {
            "id": "unique_id",
            "section": "string",
            "clause_type": "string",
            "title": "string",
            "content": "full text",
            "risk_level": "low/medium/high/critical",
            "financial_terms": {
                "amounts": ["amount1", "amount2"],
                "payment_schedule": "string",
                "penalties": ["penalty1", "penalty2"]
            },
            "key_dates": ["date1", "date2"],
            "related_clauses": ["id1", "id2"]
        }
    ],
    "visual_elements": [
        {
            "type": "table/chart/diagram",
            "page": "number",
            "content": "structured data",
            "interpretation": "what it means"
        }
    ],
    "compliance_checklist": [
        {
            "requirement": "string",
            "status": "compliant/non-compliant/unknown",
            "evidence": "string",
            "action_needed": "string"
        }
    ],
    "extracted_data": {
        "financial_amounts": ["amount1", "amount2"],
        "contact_info": {"emails": [], "phones": [], "addresses": []},
        "key_terms": ["term1", "term2"],
        "obligations": ["obligation1", "obligation2"]
    }
}
"""

    def _parse_structured_response(self, response_text: str, processing_type: str) -> Dict[str, Any]:
        """Parse and validate structured response from Gemini"""

        try:
            # Clean response text
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]

            # Parse JSON
            result = json.loads(cleaned_text)

            # Validate and enhance based on processing type
            if processing_type == "structured":
                return self._validate_structured_result(result)
            else:
                return self._validate_comprehensive_result(result)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse structured response: {e}")
            logger.error(f"Response: {response_text[:500]}...")
            raise Exception("Failed to parse AI response as JSON")

    def _validate_structured_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate structured analysis result"""

        # Ensure required sections exist
        required_sections = [
            "contract_metadata", "structured_clauses", "visual_elements",
            "compliance_checklist", "extracted_data"
        ]

        for section in required_sections:
            if section not in result:
                result[section] = {}

        # Validate clauses
        if "structured_clauses" in result and result["structured_clauses"]:
            validated_clauses = []
            for clause in result["structured_clauses"]:
                if isinstance(clause, dict) and "content" in clause:
                    validated_clauses.append(clause)
            result["structured_clauses"] = validated_clauses

        # Add metadata
        result["validation_status"] = "completed"
        result["structured_extraction"] = True

        return result

    def _validate_comprehensive_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate comprehensive analysis result"""

        # Ensure required sections exist
        required_sections = ["clauses", "risk_analysis", "key_insights", "recommendations"]

        for section in required_sections:
            if section not in result:
                result[section] = []

        # Validate clauses
        if "clauses" in result and result["clauses"]:
            validated_clauses = []
            for clause in result["clauses"]:
                if isinstance(clause, dict) and "clause_text" in clause:
                    # Add default values for missing fields
                    clause.setdefault("risk_level", "medium")
                    clause.setdefault("risk_score", 5.0)
                    clause.setdefault("confidence", 0.8)
                    clause.setdefault("legal_implications", [])
                    clause.setdefault("negotiation_points", [])
                    validated_clauses.append(clause)
            result["clauses"] = validated_clauses

        # Calculate overall metrics
        if result["clauses"]:
            risk_scores = [c.get("risk_score", 5) for c in result["clauses"]]
            result["risk_analysis"]["overall_risk_score"] = sum(risk_scores) / len(risk_scores)

            # Count risk distribution
            risk_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            for clause in result["clauses"]:
                risk_level = clause.get("risk_level", "medium").lower()
                if risk_level in risk_counts:
                    risk_counts[risk_level] += 1
            result["risk_analysis"]["risk_distribution"] = risk_counts

        # Add metadata
        result["validation_status"] = "completed"
        result["comprehensive_analysis"] = True

        return result

    async def compare_multiple_documents(
        self,
        documents: List[Dict[str, Any]],
        comparison_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """Compare multiple documents using Gemini's multi-document capabilities"""

        try:
            if len(documents) < 2:
                raise ValueError("At least 2 documents required for comparison")

            logger.info(f"Comparing {len(documents)} documents")

            # Prepare documents for comparison
            document_parts = []
            document_summaries = []

            for i, doc in enumerate(documents):
                if doc.get("format") == "pdf":
                    # Upload PDF via File API
                    doc_io = io.BytesIO(doc["data"])
                    uploaded_file = self.file_client.files.upload(
                        file=doc_io,
                        config=dict(mime_type=doc["mime_type"])
                    )
                    document_parts.append(uploaded_file)
                    document_summaries.append(f"Document {i+1}: {doc['filename']}")
                else:
                    # Text document
                    document_parts.append(doc["data"])
                    document_summaries.append(f"Document {i+1}: {doc['filename']}")

            # Create comparison prompt
            comparison_prompt = f"""
Compare these {len(documents)} legal documents and provide comprehensive analysis:

DOCUMENTS:
{chr(10).join(document_summaries)}

COMPARISON REQUIREMENTS:
1. Identify key differences between all documents
2. Compare risk profiles and exposures
3. Analyze changes in legal obligations
4. Review financial implications
5. Assess compliance differences
6. Provide negotiation insights

Focus on:
- Clause modifications and additions
- Risk level changes
- Financial impact variations
- Legal implication differences
- Compliance requirement changes

Format as JSON:
{{
    "comparison_summary": "overall comparison overview",
    "document_differences": {{
        "document_1_vs_2": ["difference1", "difference2"],
        "document_2_vs_3": ["difference1", "difference2"]
    }},
    "risk_comparison": {{
        "risk_trends": ["trend1", "trend2"],
        "risk_increases": ["area1", "area2"],
        "risk_decreases": ["area1", "area2"]
    }},
    "financial_impact": {{
        "cost_changes": ["change1", "change2"],
        "liability_shifts": ["shift1", "shift2"],
        "payment_modifications": ["mod1", "mod2"]
    }},
    "compliance_changes": {{
        "new_requirements": ["req1", "req2"],
        "removed_obligations": ["obl1", "obl2"],
        "regulatory_updates": ["update1", "update2"]
    }},
    "negotiation_insights": [
        "insight1",
        "insight2",
        "insight3"
    ],
    "recommendations": [
        "recommendation1",
        "recommendation2"
    ]
}}
"""

            # Process comparison
            response = self.model.generate_content([
                *document_parts,
                comparison_prompt
            ])

            # Parse comparison result
            result = json.loads(response.text.strip())

            # Add metadata
            result["comparison_metadata"] = {
                "document_count": len(documents),
                "comparison_type": comparison_type,
                "processing_time": time.time(),
                "document_names": [doc["filename"] for doc in documents]
            }

            return result

        except Exception as e:
            logger.error(f"Multi-document comparison failed: {e}")
            return {
                "comparison_summary": "Comparison failed",
                "document_differences": {},
                "risk_comparison": {},
                "financial_impact": {},
                "compliance_changes": {},
                "negotiation_insights": [],
                "recommendations": ["Review documents manually"],
                "error": str(e)
            }

    async def extract_structured_data(
        self,
        document_data: Dict[str, Any],
        data_types: List[str] = None
    ) -> Dict[str, Any]:
        """Extract specific structured data from document"""

        if data_types is None:
            data_types = ["financial", "dates", "parties", "obligations"]

        try:
            extraction_prompt = f"""
Extract structured data from this contract document. Focus on these data types: {', '.join(data_types)}

EXTRACTION REQUIREMENTS:
1. Financial terms (amounts, payment schedules, penalties)
2. Important dates (effective dates, deadlines, termination dates)
3. Parties involved (names, roles, contact information)
4. Key obligations and responsibilities
5. Compliance requirements and regulatory references
6. Geographic and jurisdictional information

Format as structured JSON with clear categories:
{{
    "financial_data": {{
        "monetary_amounts": [
            {{"amount": "value", "currency": "USD", "description": "what for", "frequency": "one-time/monthly"}}
        ],
        "payment_schedules": [
            {{"due_date": "date", "amount": "value", "conditions": "text"}}
        ],
        "penalties": [
            {{"trigger": "condition", "penalty": "consequence", "amount": "value"}}
        ]
    }},
    "temporal_data": {{
        "effective_dates": ["date1", "date2"],
        "deadlines": ["deadline1", "deadline2"],
        "durations": ["duration1", "duration2"],
        "renewal_terms": "text"
    }},
    "party_data": {{
        "primary_parties": [
            {{"name": "string", "role": "string", "type": "individual/corporation"}}
        ],
        "contact_information": {{
            "addresses": ["address1", "address2"],
            "emails": ["email1", "email2"],
            "phones": ["phone1", "phone2"]
        }}
    }},
    "obligations_data": {{
        "party_obligations": {{
            "party1": ["obligation1", "obligation2"],
            "party2": ["obligation1", "obligation2"]
        }},
        "mutual_obligations": ["mutual1", "mutual2"],
        "conditional_obligations": ["conditional1", "conditional2"]
    }},
    "compliance_data": {{
        "regulatory_references": ["GDPR", "CCPA", "SOX"],
        "compliance_obligations": ["obligation1", "obligation2"],
        "reporting_requirements": ["report1", "report2"],
        "audit_rights": "text"
    }},
    "geographic_data": {{
        "jurisdictions": ["jurisdiction1", "jurisdiction2"],
        "governing_law": "string",
        "dispute_resolution": "string",
        "applicable_laws": ["law1", "law2"]
    }}
}}
"""

            # Process extraction
            if document_data["format"] == "pdf":
                response = self.model.generate_content([
                    types.Part.from_bytes(
                        data=document_data["data"],
                        mime_type=document_data["mime_type"]
                    ),
                    extraction_prompt
                ])
            else:
                response = self.model.generate_content(f"{extraction_prompt}\n\nDOCUMENT:\n{document_data['data']}")

            # Parse structured data
            result = json.loads(response.text.strip())

            # Add metadata
            result["extraction_metadata"] = {
                "data_types_requested": data_types,
                "extraction_confidence": 0.9,
                "document_format": document_data["format"]
            }

            return result

        except Exception as e:
            logger.error(f"Structured data extraction failed: {e}")
            return {
                "financial_data": {},
                "temporal_data": {},
                "party_data": {},
                "obligations_data": {},
                "compliance_data": {},
                "geographic_data": {},
                "error": str(e)
            }
