import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

async def check_postgis():
    engine = create_async_engine(os.getenv("DATABASE_URL"))
    
    async with engine.connect() as conn:
        # Check if PostGIS is installed
        result = await conn.execute(text("SELECT PostGIS_version()"))
        version = result.scalar()
        print(f"✅ PostGIS Version: {version}")
        
    await engine.dispose()

asyncio.run(check_postgis())