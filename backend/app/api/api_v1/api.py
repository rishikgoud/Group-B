"""
API router configuration for LegalEase AI
"""

from fastapi import APIRouter
from app.api.endpoints import contracts, analysis, chat, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
