# 🚀 LegalEase AI - PDF/Image Analysis Setup Guide

## 📁 **CSV Dataset Placement**

Place your downloaded Kaggle CSV file here:
```
backend/data/contracts_clauses_dataset.csv
```

The system will automatically detect and load it when the server starts.

## 🔑 **Environment Setup**

### 1. **Backend Environment Variables**

Create `backend/.env` file:
```env
# Database
DATABASE_URL=sqlite:///./data/legalease.db

# AI APIs
GEMINI_API_KEY=your_gemini_api_key_here

# Application
DEBUG=true
```

### 2. **Install Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

## 🧠 **Core Features Implemented**

### ✅ **PDF Analysis**
- **Text Extraction**: Using PyPDF2 and pdfplumber
- **OCR Support**: For scanned PDFs (requires Tesseract setup)
- **Multi-page Support**: Handles complex contracts

### ✅ **Image Analysis** 
- **OCR Processing**: Using Tesseract OCR
- **Format Support**: PNG, JPG, JPEG
- **Text Preprocessing**: Cleans OCR artifacts

### ✅ **AI-Powered Analysis**
- **Gemini Integration**: Uses Google's Gemini Pro model
- **Clause Extraction**: Identifies and classifies contract clauses
- **Risk Assessment**: Rates clauses as High/Medium/Low risk
- **Plain English**: Translates legal jargon to simple terms

### ✅ **Clause Classification**
- **14 Clause Types**: Confidentiality, IP, Liability, etc.
- **Risk Scoring**: 1-10 scale with detailed explanations
- **Recommendations**: Actionable advice for each clause

## 🔧 **API Endpoints**

### **Contract Analysis**
```http
POST /api/v1/analysis/analyze
{
  "contract_id": 1,
  "analysis_type": "full"
}
```

### **Clause Explanation**
```http
POST /api/v1/analysis/explain-clause
{
  "clause_text": "The Company shall maintain...",
  "clause_type": "confidentiality"
}
```

### **Clause Comparison**
```http
POST /api/v1/analysis/compare-clauses
{
  "clause1_text": "First clause...",
  "clause2_text": "Second clause..."
}
```

## 📊 **Analysis Output**

### **Contract Analysis Response**
```json
{
  "analysis_id": 123,
  "total_clauses": 15,
  "overall_risk_score": 6.5,
  "risk_summary": {
    "high": 2,
    "medium": 5,
    "low": 8
  },
  "clauses": [
    {
      "clause_text": "The Company shall maintain strict confidentiality...",
      "clause_type": "confidentiality",
      "risk_level": "medium",
      "risk_score": 6.5,
      "simplified_explanation": "You must keep company information secret",
      "recommendations": [
        "Review what information is considered confidential",
        "Understand the duration of confidentiality"
      ]
    }
  ],
  "key_insights": [
    "Strong IP assignment clause may limit personal projects",
    "Confidentiality obligations extend beyond employment"
  ],
  "summary": "Contract contains standard terms with moderate risk"
}
```

## 🎯 **Supported File Types**

| Type | Status | Features |
|------|--------|----------|
| **PDF** | ✅ | Text extraction, OCR support |
| **DOCX** | ✅ | Direct text extraction |
| **TXT** | ✅ | Plain text processing |
| **PNG/JPG** | ✅ | OCR text extraction |

## ⚙️ **Configuration**

### **Gemini API Setup**
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file: `GEMINI_API_KEY=your_key_here`

### **Tesseract OCR Setup** (Optional)
For image OCR, install Tesseract:
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

## 🚀 **Testing the Pipeline**

### **1. Start Backend**
```bash
cd backend
python main.py
```

### **2. Upload Contract**
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/upload" \
  -F "file=@sample_contract.pdf" \
  -F "title=Test Contract"
```

### **3. Analyze Contract**
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
  -H "Content-Type: application/json" \
  -d '{"contract_id": 1, "analysis_type": "full"}'
```

## 🔍 **Clause Types Supported**

1. **confidentiality** - Non-disclosure agreements
2. **intellectual_property** - IP rights and assignments
3. **liability** - Responsibility and damages
4. **termination** - Contract ending conditions
5. **payment** - Financial obligations
6. **non_compete** - Competition restrictions
7. **indemnification** - Loss protection
8. **governing_law** - Legal jurisdiction
9. **dispute_resolution** - Conflict resolution
10. **force_majeure** - Unforeseen circumstances
11. **assignment** - Rights transfer
12. **amendment** - Contract changes
13. **warranty** - Guarantees and promises
14. **limitation_of_liability** - Damage caps

## ⚠️ **Risk Assessment Criteria**

### **HIGH RISK (8-10)**
- Unlimited liability
- Broad IP assignment
- Restrictive non-compete
- One-sided terms

### **MEDIUM RISK (4-7)**
- Standard confidentiality
- Payment terms
- Termination conditions

### **LOW RISK (1-3)**
- Governing law
- Basic definitions
- Standard obligations

## 🎉 **Ready to Use!**

Your LegalEase AI system is now ready to:
- 📄 **Upload** PDFs, images, and documents
- 🧠 **Analyze** contracts with AI
- 🚦 **Assess** risk levels automatically
- 🗣️ **Simplify** legal language
- 📊 **Generate** detailed reports

Start by uploading a contract and watch the AI extract clauses, assess risks, and provide plain English explanations!
