# test_ny_heart_ratings.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

async def check_ny_heart_ratings():
    engine = create_async_engine(os.getenv("DATABASE_URL"))
    
    async with engine.connect() as conn:
        result = await conn.execute(text("""
            SELECT DISTINCT providers.name, providers.city, providers.zip_code, ratings.rating
            FROM providers
            JOIN procedures ON providers.provider_id = procedures.provider_id
            JOIN ratings ON providers.provider_id = ratings.provider_id
            WHERE procedures.drg_description ILIKE '%cardiac%' 
            AND providers.state = 'NY'
            ORDER BY ratings.rating DESC
            LIMIT 20
        """))
        
        print("NY Hospitals with heart procedures and their ratings:")
        for row in result:
            name, city, zip_code, rating = row
            print(f"{name} ({city}, {zip_code}) - Rating: {rating}/10")
    
    await engine.dispose()

asyncio.run(check_ny_heart_ratings())