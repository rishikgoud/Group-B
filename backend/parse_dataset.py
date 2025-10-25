"""
CSV parsing script for Kaggle Contracts Clauses Dataset
"""

import pandas as pd
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.core.database import SessionLocal, init_db
from app.models.database import Clause
from services.dataset_loader import DatasetLoaderService

def parse_kaggle_dataset(csv_file_path: str = None):
    """
    Parse the Kaggle Contracts Clauses Dataset CSV file
    
    Args:
        csv_file_path: Path to the CSV file. If None, uses default sample data.
    """
    print("🚀 Starting Kaggle Dataset Parsing...")
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Initialize dataset loader
        loader = DatasetLoaderService(db)
        
        if csv_file_path and os.path.exists(csv_file_path):
            print(f"📁 Using provided CSV file: {csv_file_path}")
            # Override the dataset file path
            loader.dataset_file = csv_file_path
            
            # Read and process the CSV
            df = pd.read_csv(csv_file_path)
            print(f"📊 Found {len(df)} rows in CSV")
            
            # Check if CSV has required columns
            required_columns = ['clause_type', 'text']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"❌ Missing required columns: {missing_columns}")
                print("Required columns: clause_type, text")
                print("Optional columns: simplified_text, risk_level")
                return False
            
            # Save the CSV to the data directory
            os.makedirs("data", exist_ok=True)
            df.to_csv(loader.dataset_file, index=False)
            print(f"💾 CSV saved to: {loader.dataset_file}")
        
        # Load dataset to database
        success = loader.load_dataset_to_db()
        
        if success:
            count = loader.get_clauses_count()
            print(f"✅ Successfully loaded {count} clauses into database")
            
            # Show statistics
            print("\n📈 Dataset Statistics:")
            print(f"Total clauses: {count}")
            
            # Count by clause type
            clause_types = db.query(Clause.clause_type).filter(
                Clause.source_dataset == "kaggle_contracts_clauses"
            ).distinct().all()
            
            print(f"Clause types: {len(clause_types)}")
            for clause_type in clause_types:
                type_count = db.query(Clause).filter(
                    Clause.clause_type == clause_type[0],
                    Clause.source_dataset == "kaggle_contracts_clauses"
                ).count()
                print(f"  - {clause_type[0]}: {type_count}")
            
            # Count by risk level
            risk_levels = db.query(Clause.risk_level).filter(
                Clause.source_dataset == "kaggle_contracts_clauses"
            ).distinct().all()
            
            print(f"Risk levels: {len(risk_levels)}")
            for risk_level in risk_levels:
                if risk_level[0]:  # Skip None values
                    risk_count = db.query(Clause).filter(
                        Clause.risk_level == risk_level[0],
                        Clause.source_dataset == "kaggle_contracts_clauses"
                    ).count()
                    print(f"  - {risk_level[0]}: {risk_count}")
            
            return True
        else:
            print("❌ Failed to load dataset")
            return False
            
    except Exception as e:
        print(f"❌ Error parsing dataset: {e}")
        return False
    finally:
        db.close()

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Parse Kaggle Contracts Clauses Dataset")
    parser.add_argument(
        "--csv", 
        type=str, 
        help="Path to the CSV file to parse"
    )
    
    args = parser.parse_args()
    
    success = parse_kaggle_dataset(args.csv)
    
    if success:
        print("\n🎉 Dataset parsing completed successfully!")
        print("You can now start the FastAPI server with: uvicorn main:app --reload")
    else:
        print("\n💥 Dataset parsing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
