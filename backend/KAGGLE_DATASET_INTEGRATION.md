# Kaggle Contracts Clauses Dataset Integration

## 🎯 Overview

The LegalEase AI backend now integrates with the Kaggle Contracts Clauses Dataset, providing a rich repository of legal clauses for analysis, comparison, and learning purposes.

## 📊 Dataset Schema

### SQLAlchemy Model (`Clause`)
```python
class Clause(Base):
    __tablename__ = "clauses"
    
    id = Column(Integer, primary_key=True, index=True)
    clause_type = Column(String(100), nullable=False, index=True)
    text = Column(Text, nullable=False)
    simplified_text = Column(Text, nullable=True)
    risk_level = Column(String(20), nullable=True, index=True)  # high, medium, low
    source_dataset = Column(String(100), default="kaggle_contracts_clauses")
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Pydantic Response Model
```python
class ClauseResponse(BaseModel):
    id: int
    clause_type: str
    text: str
    simplified_text: Optional[str] = None
    risk_level: Optional[str] = None
    source_dataset: str
    created_at: datetime
```

## 🚀 Features Implemented

### ✅ Automatic Dataset Loading
- **Startup Integration**: Dataset loads automatically when server starts
- **Duplicate Prevention**: Checks if dataset is already loaded
- **Sample Data**: Creates sample clauses for testing (since Kaggle requires authentication)

### ✅ Dataset Management Service
- **Location**: `services/dataset_loader.py`
- **Functions**:
  - `load_dataset_to_db()` - Main loading function
  - `get_clauses_count()` - Count total clauses
  - `get_clauses_by_type()` - Filter by clause type
  - `get_clauses_by_risk_level()` - Filter by risk level
  - `search_clauses()` - Advanced search with filters

### ✅ CSV Parsing Script
- **Location**: `backend/parse_dataset.py`
- **Usage**: `python parse_dataset.py --csv path/to/dataset.csv`
- **Features**:
  - Validates CSV structure
  - Shows loading statistics
  - Handles errors gracefully

### ✅ API Endpoints
- **Base URL**: `/api/v1/dataset`

#### Available Endpoints:

1. **Get Clauses** - `GET /api/v1/dataset/clauses`
   - Query parameters: `clause_type`, `risk_level`, `search_text`, `page`, `page_size`
   - Returns paginated list of clauses

2. **Get Clause by ID** - `GET /api/v1/dataset/clauses/{clause_id}`
   - Returns specific clause details

3. **Get Clause Types** - `GET /api/v1/dataset/clauses/types/list`
   - Returns list of available clause types

4. **Get Risk Levels** - `GET /api/v1/dataset/clauses/risk-levels/list`
   - Returns list of available risk levels

5. **Dataset Statistics** - `GET /api/v1/dataset/stats`
   - Returns comprehensive dataset statistics

6. **Reload Dataset** - `POST /api/v1/dataset/reload`
   - Admin endpoint to reload dataset

## 📋 Sample Data Included

The system includes sample clauses for testing:

| Clause Type | Risk Level | Count |
|-------------|------------|-------|
| confidentiality | medium | 1 |
| intellectual_property | high | 1 |
| liability | high | 1 |
| termination | low | 1 |
| payment | medium | 1 |
| non_compete | high | 1 |
| indemnification | medium | 1 |
| governing_law | low | 1 |
| dispute_resolution | medium | 1 |
| force_majeure | low | 1 |

## 🔧 Usage Examples

### 1. Start the Server
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Check Dataset Status
```bash
curl http://localhost:8000/api/v1/dataset/stats
```

### 3. Search Clauses
```bash
# Get all clauses
curl "http://localhost:8000/api/v1/dataset/clauses"

# Filter by clause type
curl "http://localhost:8000/api/v1/dataset/clauses?clause_type=confidentiality"

# Filter by risk level
curl "http://localhost:8000/api/v1/dataset/clauses?risk_level=high"

# Search in text
curl "http://localhost:8000/api/v1/dataset/clauses?search_text=confidentiality"

# Pagination
curl "http://localhost:8000/api/v1/dataset/clauses?page=1&page_size=5"
```

### 4. Parse Custom CSV
```bash
python parse_dataset.py --csv /path/to/your/dataset.csv
```

## 📁 File Structure

```
backend/
├── app/models/
│   ├── database.py          # Updated with Clause model
│   └── schemas.py           # Updated with Clause Pydantic models
├── routes/
│   └── dataset.py           # Dataset API endpoints
├── services/
│   └── dataset_loader.py    # Dataset loading service
├── data/
│   └── contracts_clauses_dataset.csv  # Sample dataset
├── parse_dataset.py         # CSV parsing script
└── main.py                  # Updated with dataset loading
```

## 🔄 Integration with Contract Analysis

The dataset can be used to enhance contract analysis:

1. **Clause Comparison**: Compare uploaded contract clauses with dataset examples
2. **Risk Assessment**: Use dataset risk levels as reference
3. **Simplified Explanations**: Leverage dataset simplified_text for better explanations
4. **Learning Mode**: Users can explore different clause types and their implications

## 🚀 Next Steps

### For Production Use:

1. **Kaggle Authentication**:
   ```python
   # Add to services/dataset_loader.py
   import kaggle
   kaggle.api.authenticate()
   ```

2. **Real Dataset Download**:
   ```python
   def _download_real_dataset(self):
       kaggle.api.dataset_download_files(
           'mohammedalrashidan/contracts-clauses-datasets',
           path=self.data_dir,
           unzip=True
       )
   ```

3. **Enhanced Processing**:
   - Add more clause types
   - Implement risk scoring algorithms
   - Add clause similarity matching

4. **API Enhancements**:
   - Add clause similarity search
   - Implement clause recommendations
   - Add export functionality

## 🐛 Troubleshooting

### Common Issues:

1. **Dataset Not Loading**:
   - Check database connection
   - Verify file permissions
   - Check logs for specific errors

2. **Empty Results**:
   - Ensure dataset was loaded successfully
   - Check if filters are too restrictive
   - Verify clause types and risk levels exist

3. **CSV Parsing Errors**:
   - Ensure CSV has required columns: `clause_type`, `text`
   - Check for encoding issues
   - Validate CSV format

### Debug Commands:

```bash
# Check if dataset is loaded
curl http://localhost:8000/api/v1/dataset/stats

# Reload dataset
curl -X POST http://localhost:8000/api/v1/dataset/reload

# Check database directly
sqlite3 data/legalease.db "SELECT COUNT(*) FROM clauses;"
```

## 📈 Performance Considerations

- **Indexing**: Database indexes on `clause_type`, `risk_level`, and `source_dataset`
- **Pagination**: All list endpoints support pagination
- **Caching**: Consider adding Redis for frequently accessed data
- **Search Optimization**: Full-text search indexes for large datasets

The Kaggle dataset integration provides a solid foundation for legal clause analysis and comparison, making LegalEase AI more powerful and educational for users.
