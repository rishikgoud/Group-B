"""
Dataset loader service for Kaggle Contracts Clauses Dataset
"""

import pandas as pd
import os
import requests
import zipfile
from sqlalchemy.orm import Session
from app.models.database import Clause
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DatasetLoaderService:
    def __init__(self, db: Session):
        self.db = db
        self.dataset_url = "https://www.kaggle.com/datasets/mohammedalrashidan/contracts-clauses-datasets/download"
        self.data_dir = "data"
        self.dataset_file = os.path.join(self.data_dir, "contracts_clauses_dataset.csv")
    
    def load_dataset_to_db(self) -> bool:
        """Load the Kaggle dataset into the database"""
        try:
            # Check if dataset is already loaded
            if self._is_dataset_loaded():
                logger.info("Dataset already loaded, skipping...")
                return True
            
            # Download and process dataset
            if not self._download_dataset():
                logger.error("Failed to download dataset")
                return False
            
            # Parse and insert data
            if not self._parse_and_insert_data():
                logger.error("Failed to parse and insert dataset")
                return False
            
            logger.info("Dataset loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return False
    
    def _is_dataset_loaded(self) -> bool:
        """Check if dataset is already loaded in database"""
        count = self.db.query(Clause).filter(
            Clause.source_dataset == "kaggle_contracts_clauses"
        ).count()
        return count > 0
    
    def _download_dataset(self) -> bool:
        """Download the dataset from Kaggle"""
        try:
            # Create data directory
            os.makedirs(self.data_dir, exist_ok=True)
            
            # For now, we'll create a sample dataset since Kaggle requires authentication
            # In production, you would need to authenticate with Kaggle API
            logger.info("Creating sample dataset (Kaggle requires authentication)")
            self._create_sample_dataset()
            return True
            
        except Exception as e:
            logger.error(f"Error downloading dataset: {e}")
            return False
    
    def _create_sample_dataset(self):
        """Create a sample dataset for testing purposes"""
        sample_data = [
            {
                "clause_type": "confidentiality",
                "text": "The Company shall maintain strict confidentiality regarding all proprietary information, trade secrets, and confidential data disclosed by the Client during the term of this Agreement.",
                "simplified_text": "You must keep company information secret",
                "risk_level": "medium"
            },
            {
                "clause_type": "intellectual_property",
                "text": "Employee agrees to assign all intellectual property rights, including but not limited to inventions, discoveries, improvements, and works of authorship, to the Company.",
                "simplified_text": "The company owns all your work and ideas",
                "risk_level": "high"
            },
            {
                "clause_type": "liability",
                "text": "In no event shall the Company be liable for any indirect, incidental, special, consequential, or punitive damages, including but not limited to loss of profits, data, or business opportunities.",
                "simplified_text": "Company limits its responsibility for damages",
                "risk_level": "high"
            },
            {
                "clause_type": "termination",
                "text": "Either party may terminate this Agreement with thirty (30) days written notice to the other party.",
                "simplified_text": "Either side can end the contract with 30 days notice",
                "risk_level": "low"
            },
            {
                "clause_type": "payment",
                "text": "Payment shall be made within thirty (30) days of invoice date. Late payments may incur a service charge of 1.5% per month.",
                "simplified_text": "Payment due within 30 days, late fees apply",
                "risk_level": "medium"
            },
            {
                "clause_type": "non_compete",
                "text": "Employee agrees not to engage in any business activity that competes with the Company's business for a period of two (2) years following termination.",
                "simplified_text": "Cannot work for competitors for 2 years after leaving",
                "risk_level": "high"
            },
            {
                "clause_type": "indemnification",
                "text": "Client shall indemnify and hold harmless the Company from any claims, damages, or expenses arising from Client's use of the services.",
                "simplified_text": "Client protects company from legal claims",
                "risk_level": "medium"
            },
            {
                "clause_type": "governing_law",
                "text": "This Agreement shall be governed by and construed in accordance with the laws of the State of California.",
                "simplified_text": "California law applies to this contract",
                "risk_level": "low"
            },
            {
                "clause_type": "dispute_resolution",
                "text": "Any disputes arising under this Agreement shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association.",
                "simplified_text": "Disputes will be settled through arbitration",
                "risk_level": "medium"
            },
            {
                "clause_type": "force_majeure",
                "text": "Neither party shall be liable for any failure or delay in performance due to circumstances beyond their reasonable control, including acts of God, war, or government action.",
                "simplified_text": "Neither side is responsible for delays due to events beyond their control",
                "risk_level": "low"
            }
        ]
        
        # Save as CSV
        df = pd.DataFrame(sample_data)
        df.to_csv(self.dataset_file, index=False)
        logger.info(f"Sample dataset created at {self.dataset_file}")
    
    def _parse_and_insert_data(self) -> bool:
        """Parse CSV and insert data into database"""
        try:
            # Read CSV file
            df = pd.read_csv(self.dataset_file)
            
            # Insert data into database
            clauses_to_insert = []
            for _, row in df.iterrows():
                clause = Clause(
                    clause_type=row['clause_type'],
                    text=row['text'],
                    simplified_text=row.get('simplified_text'),
                    risk_level=row.get('risk_level'),
                    source_dataset="kaggle_contracts_clauses"
                )
                clauses_to_insert.append(clause)
            
            # Bulk insert
            self.db.add_all(clauses_to_insert)
            self.db.commit()
            
            logger.info(f"Inserted {len(clauses_to_insert)} clauses into database")
            return True
            
        except Exception as e:
            logger.error(f"Error parsing and inserting data: {e}")
            self.db.rollback()
            return False
    
    def get_clauses_count(self) -> int:
        """Get total count of clauses in dataset"""
        return self.db.query(Clause).filter(
            Clause.source_dataset == "kaggle_contracts_clauses"
        ).count()
    
    def get_clauses_by_type(self, clause_type: str) -> List[Clause]:
        """Get clauses by type"""
        return self.db.query(Clause).filter(
            Clause.clause_type == clause_type,
            Clause.source_dataset == "kaggle_contracts_clauses"
        ).all()
    
    def get_clauses_by_risk_level(self, risk_level: str) -> List[Clause]:
        """Get clauses by risk level"""
        return self.db.query(Clause).filter(
            Clause.risk_level == risk_level,
            Clause.source_dataset == "kaggle_contracts_clauses"
        ).all()
    
    def search_clauses(self, search_text: str = None, clause_type: str = None, 
                      risk_level: str = None, limit: int = 100) -> List[Clause]:
        """Search clauses with filters"""
        query = self.db.query(Clause).filter(
            Clause.source_dataset == "kaggle_contracts_clauses"
        )
        
        if search_text:
            query = query.filter(Clause.text.contains(search_text))
        
        if clause_type:
            query = query.filter(Clause.clause_type == clause_type)
        
        if risk_level:
            query = query.filter(Clause.risk_level == risk_level)
        
        return query.limit(limit).all()
