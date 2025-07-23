import sys
sys.path.append('.')  # Add current directory to path

import pandas as pd
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from app.models import Base, Provider, Procedure, Rating

# Load environment variables
load_dotenv()

# Get regular (sync) database URL for ETL
DATABASE_URL = os.getenv("DATABASE_URL").replace("+asyncpg", "")

print("Starting ETL process...")
print(f"Connecting to database...")

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
        
        # Load providers
        for _, row in providers_df.iterrows():
            provider = Provider(
                provider_id=str(row['Rndrng_Prvdr_CCN']),
                name=row['Rndrng_Prvdr_Org_Name'],
                city=row['Rndrng_Prvdr_City'],
                state=row['Rndrng_Prvdr_State_Abrvtn'],
                zip_code=str(row['Rndrng_Prvdr_Zip5'])
            )
            session.add(provider)
        
        # Commit providers first
        session.commit()
        print("✅ Providers loaded!")
        
        # Load procedures
        print(f"Loading {len(df)} procedures...")
        for _, row in df.iterrows():
            procedure = Procedure(
                provider_id=str(row['Rndrng_Prvdr_CCN']),
                drg_code=str(row['DRG_Cd']),
                drg_description=row['DRG_Desc'],
                total_discharges=int(row['Tot_Dschrgs']),
                avg_covered_charges=float(row['Avg_Submtd_Cvrd_Chrg']),
                avg_total_payments=float(row['Avg_Tot_Pymt_Amt']),
                avg_medicare_payments=float(row['Avg_Mdcr_Pymt_Amt'])
            )
            session.add(procedure)
        
        # Commit procedures
        session.commit()
        print("✅ Procedures loaded!")
        
        # Generate and load ratings
        print("Generating mock ratings...")
        for provider_id in providers_df['Rndrng_Prvdr_CCN'].unique():
            rating = Rating(
                provider_id=str(provider_id),
                rating=random.randint(1, 10)  # Random rating 1-10
            )
            session.add(rating)
        
        # Commit ratings
        session.commit()
        print("✅ Ratings loaded!")
        
        print("\n🎉 ETL complete!")
        print(f"Loaded: {len(providers_df)} providers, {len(df)} procedures, {len(providers_df)} ratings")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    run_etl()