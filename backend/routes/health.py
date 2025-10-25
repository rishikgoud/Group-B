"""
Health check routes
"""

from fastapi import APIRouter, Depends
from app.core.database import get_database, check_db_connection
from app.models.schemas import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint"""
    return HealthResponse()

@router.get("/detailed")
async def detailed_health_check(db = Depends(get_database)):
    """Detailed health check with dependencies"""
    
    # Check database connection
    db_status = await check_db_connection()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "service": "LegalEase AI",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z",
        "dependencies": {
            "database": "connected" if db_status else "disconnected",
            "ai_services": "available"  # TODO: Add actual AI service checks
        },
        "uptime": "0d 0h 0m",  # TODO: Implement actual uptime tracking
        "environment": "development"
    }
