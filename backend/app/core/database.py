"""
MongoDB database configuration and connection
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.mongodb_models import (
    Contract, ContractAnalysis, ContractClause, 
    Clause, User, AnalysisSession
)
import asyncio
from typing import AsyncGenerator

# MongoDB client
client: AsyncIOMotorClient = None
database = None

async def init_db():
    """Initialize MongoDB database and collections"""
    global client, database
    
    try:
        # Create MongoDB client
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        database = client[settings.DATABASE_NAME]
        
        # Initialize Beanie with all document models
        await init_beanie(
            database=database,
            document_models=[
                Contract,
                ContractAnalysis, 
                ContractClause,
                Clause,
                User,
                AnalysisSession
            ]
        )
        
        print("✅ MongoDB database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB initialization failed: {e}")
        return False

async def get_database():
    """Get database instance"""
    if database is None:
        await init_db()
    return database

async def close_db():
    """Close database connection"""
    if client:
        client.close()
        print("✅ MongoDB connection closed")

async def check_db_connection():
    """Check if MongoDB is accessible"""
    try:
        if client is None:
            await init_db()
        
        # Test database connection
        await client.admin.command('ping')
        print("✅ MongoDB connection verified")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

# For backward compatibility with existing code
def get_db():
    """Get database session (for compatibility)"""
    return database