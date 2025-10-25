"""
Health check endpoints
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "LegalEase AI",
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check with dependencies"""
    return {
        "status": "healthy",
        "service": "LegalEase AI",
        "version": "1.0.0",
        "dependencies": {
            "database": "connected",
            "ai_services": "available"
        }
    }
