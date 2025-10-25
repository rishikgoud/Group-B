"""
LegalEase AI - FastAPI Backend Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.core.config import settings
from app.core.database import init_db, check_db_connection
from routes import upload, analysis, health, dataset
from services.dataset_loader import DatasetLoaderService

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description="AI-powered contract analysis and legal document understanding",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(upload.router, prefix="/api/v1/contracts", tags=["contracts"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(dataset.router, prefix="/api/v1/dataset", tags=["dataset"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "⚖️ LegalEase AI - Contract Analyzer",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.on_event("startup")
async def startup_event():
    """Initialize database and load dataset on startup"""
    print("🚀 Starting LegalEase AI Backend...")
    
    # Initialize database
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return
    
    # Check database connection
    if not check_db_connection():
        print("❌ Database connection failed")
        return
    print("✅ Database connection verified")
    
    # Load Kaggle dataset
    try:
        from app.core.database import SessionLocal
        db = SessionLocal()
        loader = DatasetLoaderService(db)
        
        print("📊 Loading Kaggle Contracts Clauses Dataset...")
        success = loader.load_dataset_to_db()
        
        if success:
            count = loader.get_clauses_count()
            print(f"✅ Dataset loaded successfully! ({count} clauses)")
        else:
            print("⚠️ Dataset loading failed, but server will continue")
        
        db.close()
        
    except Exception as e:
        print(f"⚠️ Dataset loading error: {e}")
        print("Server will continue without dataset")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
