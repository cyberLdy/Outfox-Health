import sys
sys.path.append('.')  # Add current directory to path

import pandas as pd
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from app.models import Base, Provider, Procedure, Rating

# Rest of your code...

# Load environment variables
load_dotenv()

# Get regular (sync) database URL for ETL
DATABASE_URL = os.getenv("DATABASE_URL").replace("+asyncpg", "")

print("Starting ETL process...")
print(f"Connecting to database...")

# Create tables and load data
def run_etl():
    # Create engine (synchronous for ETL)
    engine = create_engine(DATABASE_URL)
    
    # Create all tables
    print("Creating tables...")
    Base.metadata.drop_all(engine)  # Drop existing tables
    Base.metadata.create_all(engine)  # Create new tables
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Read CSV
        print("Reading CSV file...")
        df = pd.read_csv('MUP_INP_RY24_P03_V10_DY22_PrvSvc.csv', encoding='latin-1')
        print(f"Found {len(df)} rows")
        
        # Get unique providers
        providers_df = df[['Rndrng_Prvdr_CCN', 'Rndrng_Prvdr_Org_Name', 
                          'Rndrng_Prvdr_City', 'Rndrng_Prvdr_State_Abrvtn', 
                          'Rndrng_Prvdr_Zip5']].drop_duplicates()
        
        print(f"Loading {len(providers_df)} providers...")
        
        # More ETL code will go here...
        print("ETL complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    run_etl()