import asyncio
import asyncpg

async def test_connection():
    try:
        # Your connection string without +asyncpg for direct asyncpg test
        conn = await asyncpg.connect(
            'postgresql://postgres:Outfox@db.uvtxyhozwllxqnhafuyg.supabase.co:5432/postgres'
        )
        print("✅ Connected to database successfully!")
        
        # Test query
        version = await conn.fetchval('SELECT version()')
        print(f"PostgreSQL version: {version}")
        
        await conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

# Run the test
asyncio.run(test_connection())