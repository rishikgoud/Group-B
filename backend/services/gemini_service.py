"""
Gemini AI service for contract analysis
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class EnhancedGeminiService:
    """Enhanced Gemini AI service with native PDF processing capabilities"""

    def __init__(self):
        """Initialize enhanced Gemini AI service"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use the latest Gemini model with PDF support
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Updated to use Flash model

        # Define comprehensive clause types
        self.clause_types = [
            "confidentiality", "intellectual_property", "liability",
            "termination", "payment", "non_compete", "indemnification",
            "governing_law", "dispute_resolution", "force_majeure",
            "assignment", "amendment", "warranty", "limitation_of_liability",
            "data_protection", "compliance", "insurance", "performance",
            "scope_of_work", "pricing", "delivery", "warranties"
        ]
        
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_response(response.text)
            return result
        except Exception as e:
            logger.error(f"Error analyzing contract with Gemini: {e}")
            raise Exception(f"Contract analysis failed: {str(e)}")
    
    def _create_analysis_prompt(self, contract_text: str) -> str:
        """Create a comprehensive prompt for contract analysis"""
        
        return f"""
You are a legal AI assistant specializing in contract analysis. Analyze the following contract text and extract all clauses with detailed information.

CONTRACT TEXT:
{contract_text}

INSTRUCTIONS:
1. Extract ALL clauses from the contract
2. Classify each clause by type from this list: {', '.join(self.clause_types)}
3. Assess risk level for each clause: high, medium, or low
4. Provide simplified explanations in plain English
5. Give actionable recommendations for high-risk clauses

OUTPUT FORMAT (JSON):
{{
    "clauses": [
        {{
            "clause_text": "exact text from contract",
            "clause_type": "one of the predefined types",
            "risk_level": "high/medium/low",
            "risk_score": 1-10,
            "simplified_explanation": "plain English explanation",
            "recommendations": ["actionable recommendation 1", "recommendation 2"],
            "start_position": 0,
            "end_position": 100
        }}
    ],
    "overall_risk_score": 1-10,
    "key_insights": ["insight 1", "insight 2", "insight 3"],
    "summary": "Brief overall contract summary"
}}

RISK ASSESSMENT CRITERIA:
- HIGH RISK (8-10): Unlimited liability, broad IP assignment, restrictive non-compete, one-sided terms
- MEDIUM RISK (4-7): Standard confidentiality, payment terms, termination conditions
- LOW RISK (1-3): Governing law, basic definitions, standard obligations

Return ONLY valid JSON, no additional text.
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response and extract structured data"""
        
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            # Parse JSON
            result = json.loads(cleaned_text)
            
            # Validate and clean the result
            return self._validate_result(result)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            logger.error(f"Response text: {response_text}")
            raise Exception("Failed to parse AI response")
    
    def _validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the analysis result"""
        
        # Ensure required fields exist
        if "clauses" not in result:
            result["clauses"] = []
        
        if "overall_risk_score" not in result:
            result["overall_risk_score"] = 5.0
        
        if "key_insights" not in result:
            result["key_insights"] = []
        
        if "summary" not in result:
            result["summary"] = "Contract analysis completed"
        
        # Validate and clean each clause
        validated_clauses = []
        for clause in result["clauses"]:
            validated_clause = self._validate_clause(clause)
            if validated_clause:
                validated_clauses.append(validated_clause)
        
        result["clauses"] = validated_clauses
        result["total_clauses"] = len(validated_clauses)
        
        # Calculate risk summary
        risk_summary = {"high": 0, "medium": 0, "low": 0}
        for clause in validated_clauses:
            risk_level = clause.get("risk_level", "low")
            if risk_level in risk_summary:
                risk_summary[risk_level] += 1
        
        result["risk_summary"] = risk_summary
        
        return result
    
    def _validate_clause(self, clause: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate and clean a single clause"""
        
        # Required fields
        if not clause.get("clause_text") or not clause.get("clause_type"):
            return None
        
        # Validate clause type
        clause_type = clause["clause_type"].lower()
        if clause_type not in self.clause_types:
            clause_type = "other"
        
        # Validate risk level
        risk_level = clause.get("risk_level", "low").lower()
        if risk_level not in self.risk_levels:
            risk_level = "low"
        
        # Validate risk score
        risk_score = clause.get("risk_score", 5)
        try:
            risk_score = float(risk_score)
            risk_score = max(1, min(10, risk_score))
        except (ValueError, TypeError):
            risk_score = 5
        
        # Ensure recommendations is a list
        recommendations = clause.get("recommendations", [])
        if not isinstance(recommendations, list):
            recommendations = [str(recommendations)] if recommendations else []
        
        return {
            "clause_text": clause["clause_text"].strip(),
            "clause_type": clause_type,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "simplified_explanation": clause.get("simplified_explanation", ""),
            "recommendations": recommendations,
            "start_position": clause.get("start_position", 0),
            "end_position": clause.get("end_position", 0)
        }
    
    async def explain_clause(self, clause_text: str, clause_type: str) -> Dict[str, str]:
        """Get detailed explanation for a specific clause"""
        
        prompt = f"""
Explain this legal clause in simple terms:

CLAUSE TYPE: {clause_type}
CLAUSE TEXT: {clause_text}

Provide:
1. Plain English explanation
2. Key points to understand
3. Potential risks or benefits
4. What to watch out for

Format as JSON:
{{
    "explanation": "simple explanation",
    "key_points": ["point 1", "point 2"],
    "risks": ["risk 1", "risk 2"],
    "benefits": ["benefit 1", "benefit 2"],
    "watch_out": ["warning 1", "warning 2"]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            return result
        except Exception as e:
            logger.error(f"Error explaining clause: {e}")
            return {
                "explanation": "Unable to generate explanation",
                "key_points": [],
                "risks": [],
                "benefits": [],
                "watch_out": []
            }
    
    async def compare_clauses(self, clause1: str, clause2: str) -> Dict[str, Any]:
        """Compare two clauses and highlight differences"""
        
        prompt = f"""
Compare these two legal clauses and highlight key differences:

CLAUSE 1:
{clause1}

CLAUSE 2:
{clause2}

Provide:
1. Main differences
2. Risk implications
3. Recommendations

Format as JSON:
{{
    "differences": ["difference 1", "difference 2"],
    "risk_implications": "explanation of risk differences",
    "recommendations": ["recommendation 1", "recommendation 2"]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            return result
        except Exception as e:
            logger.error(f"Error comparing clauses: {e}")
            return {
                "differences": ["Unable to compare clauses"],
                "risk_implications": "Comparison failed",
                "recommendations": ["Review clauses manually"]
            }
