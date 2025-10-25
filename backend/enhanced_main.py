"""
Enhanced FastAPI Application with Comprehensive Error Handling
Production-ready LegalEase AI backend with industry-standard features
"""

import asyncio
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
from concurrent.futures import ThreadPoolExecutor
import time

from app.core.config import settings
from app.core.database import init_db, check_db_connection, close_db, get_database
from routes import upload, analysis, health, dataset

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    description="AI-powered contract analysis and legal document understanding",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight for 1 hour
)

# Include API routers with enhanced error handling
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(upload.router, prefix="/api/v1/contracts", tags=["contracts"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(dataset.router, prefix="/api/v1/dataset", tags=["dataset"])

# Request/Response interceptors for enhanced monitoring
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing and status"""

    start_time = time.time()

    # Log request
    logger.info(f"Incoming {request.method} {request.url.path} from {request.client.host}")

    try:
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Completed {request.method} {request.url.path} - "
            f"Status: {response.status_code} - Time: {process_time:.".3f""
        )

        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)

        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Failed {request.method} {request.url.path} - "
            f"Error: {str(e)} - Time: {process_time:.".3f""
        )
        raise

# Enhanced error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with detailed logging"""

    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request failed",
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""

    logger.error(f"Validation Error: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "detail": "Invalid request data",
            "validation_errors": exc.errors(),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""

    logger.error(f"Unexpected Error: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": str(uuid.uuid4())
        }
    )

# Enhanced root endpoint
@app.get("/")
async def root():
    """Enhanced root endpoint with system status"""

    try:
        db_status = await check_db_connection()

        return {
            "message": "⚖️ LegalEase AI - Contract Analyzer",
            "version": settings.APP_VERSION,
            "status": "running",
            "database_status": "connected" if db_status else "disconnected",
            "docs": "/docs",
            "health": "/health",
            "features": [
                "Contract Upload & Processing",
                "AI-Powered Analysis",
                "Risk Assessment",
                "MongoDB Storage",
                "PDF/OCR Support",
                "Real-time Analytics"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Root endpoint error: {e}")
        return {
            "message": "⚖️ LegalEase AI - Contract Analyzer",
            "version": settings.APP_VERSION,
            "status": "error",
            "error": str(e)
        }

async def load_dataset_background():
    """
    Enhanced dataset loading with better error handling
    """
    try:
        logger.info("Loading Kaggle Contracts Clauses Dataset...")
        db = await get_database()
        from services.dataset_loader import DatasetLoaderService

        loader = DatasetLoaderService(db)
        success = await loader.load_dataset_to_db()

        if success:
            count = await loader.get_clauses_count()
            logger.info(f"✅ Dataset loaded successfully! ({count} clauses)")
        else:
            logger.warning("⚠️ Dataset loading failed, but server will continue")

    except Exception as e:
        logger.error(f"Dataset loading error: {e}")
        logger.info("Server will continue without dataset")

@app.on_event("startup")
async def enhanced_startup_event():
    """Enhanced startup with comprehensive initialization"""

    logger.info("🚀 Starting LegalEase AI Backend...")
    logger.info(f"Version: {settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    # Initialize MongoDB database with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"Initializing MongoDB (attempt {attempt + 1}/{max_retries})...")
            success = await init_db()

            if not success:
                logger.error("Database initialization failed")
                if attempt == max_retries - 1:
                    logger.critical("Failed to initialize database after all retries")
                    return
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue

            logger.info("✅ MongoDB database initialized successfully")
            break

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            if attempt == max_retries - 1:
                logger.critical("Failed to initialize database after all retries")
                return
            await asyncio.sleep(2 ** attempt)

    # Check database connection
    logger.info("Verifying database connection...")
    if not await check_db_connection():
        logger.error("Database connection verification failed")
        return

    logger.info("✅ Database connection verified")

    # Load dataset in background with enhanced error handling
    logger.info("📊 Starting background dataset loading...")
    asyncio.create_task(load_dataset_background())

    logger.info("🎉 LegalEase AI Backend startup completed successfully!")
    logger.info("📍 API available at: http://localhost:8000")
    logger.info("📖 Documentation at: http://localhost:8000/docs")

@app.on_event("shutdown")
async def enhanced_shutdown_event():
    """Enhanced shutdown with proper cleanup"""

    logger.info("🛑 Initiating LegalEase AI shutdown...")

    try:
        await close_db()
        logger.info("✅ MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error during database cleanup: {e}")

    logger.info("✅ Application shutdown complete")

# Development server configuration
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True,
        server_header=False,  # Security: Don't expose server info
        date_header=False     # Security: Don't expose timestamps
    )
