# LegalEase AI Backend Setup Guide

## 🏗️ New Modular Architecture

The backend has been restructured with a clean, modular FastAPI architecture:

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # SQLite database setup
│   └── models/
│       ├── database.py        # SQLAlchemy ORM models
│       └── schemas.py         # Pydantic request/response schemas
├── routes/
│   ├── upload.py             # Contract upload endpoints
│   ├── analysis.py           # Contract analysis endpoints
│   └── health.py             # Health check endpoints
├── services/
│   ├── contract_service.py   # Contract business logic
│   └── analyzer_service.py   # Analysis business logic
├── main.py                   # FastAPI application
├── init_db.py               # Database initialization script
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Start the Server
```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## 📊 Database Schema

### Tables Created:
- **contracts** - Store uploaded contract files
- **contract_analyses** - Analysis results and metadata
- **contract_clauses** - Individual clause analysis
- **chat_sessions** - AI chat sessions
- **chat_messages** - Individual chat messages

### Database Location:
- **SQLite file**: `./data/legalease.db`
- **Auto-created**: Database and tables are created automatically

## 🔗 API Endpoints

### Health Check
- `GET /health/` - Basic health check
- `GET /health/detailed` - Detailed health with dependencies

### Contract Management
- `POST /api/v1/contracts/upload` - Upload contract file
- `GET /api/v1/contracts/list` - List all contracts
- `GET /api/v1/contracts/{id}` - Get contract details
- `DELETE /api/v1/contracts/{id}` - Delete contract

### Contract Analysis
- `POST /api/v1/analysis/analyze` - Analyze contract
- `GET /api/v1/analysis/risk-levels` - Get risk level definitions
- `GET /api/v1/analysis/clause-types` - Get clause type definitions
- `GET /api/v1/analysis/contract/{id}/analysis` - Get analysis results

## 🛠️ Key Features

### ✅ Implemented:
- **Modular FastAPI structure** with separate routes and services
- **SQLite database** with SQLAlchemy ORM
- **Pydantic models** for request/response validation
- **File upload handling** with validation
- **Database initialization** script
- **Health check endpoints**
- **Service layer** for business logic separation

### 🔄 Mock Data:
- Contract analysis returns mock data (ready for AI integration)
- Risk scoring and clause extraction simulated
- Database operations fully functional

## 🔧 Configuration

### Environment Variables (.env):
```env
# Database
DATABASE_URL=sqlite:///./data/legalease.db

# AI APIs (for future integration)
GEMINI_API_KEY=your_gemini_api_key

# Application
SECRET_KEY=your_secret_key
DEBUG=True
```

## 📝 Usage Examples

### Upload a Contract:
```bash
curl -X POST "http://localhost:8000/api/v1/contracts/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@contract.pdf"
```

### Analyze a Contract:
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/analyze" \
  -H "Content-Type: application/json" \
  -d '{"contract_id": 1, "analysis_type": "full"}'
```

### Check Health:
```bash
curl http://localhost:8000/health/
```

## 🧪 Testing

### Test Database Connection:
```python
from app.core.database import check_db_connection
print(check_db_connection())  # Should return True
```

### Test File Upload:
1. Go to http://localhost:8000/docs
2. Use the interactive API documentation
3. Try the `/api/v1/contracts/upload` endpoint

## 🔮 Next Steps

1. **Install dependencies** and test the setup
2. **Integrate AI services** (Gemini Pro)
3. **Add file processing** (PDF parsing, OCR)
4. **Implement real analysis** logic
5. **Add authentication** and user management
6. **Deploy to production**

## 🐛 Troubleshooting

### Common Issues:
1. **Module not found**: Run `pip install -r requirements.txt`
2. **Database errors**: Run `python init_db.py`
3. **Port conflicts**: Change port in `main.py`
4. **File upload fails**: Check file size and type validation

### Debug Mode:
Set `DEBUG=True` in your `.env` file to enable:
- SQL query logging
- Detailed error messages
- Auto-reload on code changes
