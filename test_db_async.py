import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

load_dotenv()

async def test_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    print(f"Testing connection to: {DATABASE_URL[:50]}...")
    
    try:
        # Create async engine
        engine = create_async_engine(DATABASE_URL, echo=True)
        
        # Test connection
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT COUNT(*) FROM providers"))
            count = result.scalar()
            print(f"✅ Connected! Found {count} providers in database")
            
        await engine.dispose()
        
    except Exception as e:
        print(f"❌ Connection failed: {type(e).__name__}: {str(e)}")

# Run test
asyncio.run(test_connection())