"""
Database initialization script for LegalEase AI
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db, engine
from app.models.database import Base

def main():
    """Initialize the database with all tables"""
    print("🚀 Initializing LegalEase AI Database...")
    
    try:
        # Create all tables
        init_db()
        
        print("✅ Database initialization completed successfully!")
        print("📊 Database location: ./data/legalease.db")
        print("🔗 You can now start the FastAPI server with: uvicorn main:app --reload")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
