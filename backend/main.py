"""
LegalEase AI - FastAPI Backend Main Application
"""

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from concurrent.futures import ThreadPoolExecutor

from app.core.config import settings
from app.core.database import init_db, check_db_connection, close_db, get_database
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

async def load_dataset_background():
    """
    Load Kaggle Contracts Clauses Dataset in background (async-safe).
    """
    try:
        db = await get_database()
        loader = DatasetLoaderService(db)

        # Await the async loader method properly
        success = await loader.load_dataset_to_db()
        if success:
            count = await loader.get_clauses_count()
            print(f"✅ Dataset loaded successfully! ({count} clauses)")
        else:
            print("⚠️ Dataset loading failed, but server will continue")

    except Exception as e:
        print(f"⚠️ Dataset loading error: {e}")
        print("Server will continue without dataset")

@app.on_event("startup")
async def startup_event():
    """Initialize database and load dataset on startup"""
    print("🚀 Starting LegalEase AI Backend...")

    # Initialize MongoDB database
    try:
        success = await init_db()
        if not success:
            print("❌ Database initialization failed")
            return
        print("✅ MongoDB database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return

    # Check database connection
    if not await check_db_connection():
        print("❌ Database connection failed")
        return
    print("✅ Database connection verified")

    # Start dataset loading in background
    print("📊 Loading Kaggle Contracts Clauses Dataset in background...")
    asyncio.create_task(load_dataset_background())

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    await close_db()
    print("✅ Application shutdown complete")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
