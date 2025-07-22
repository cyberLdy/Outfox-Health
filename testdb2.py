import asyncpg
import asyncio

async def test_connection():
    # Connection details
    host = "db.uvtxyhozwllxqnhafuyg.supabase.co"
    port = 5432
    user = "postgres"
    password = "Outfox"
    database = "postgres"
    
    print(f"Trying to connect to:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  User: {user}")
    print(f"  Database: {database}")
    
    try:
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("✅ Connected successfully!")
        await conn.close()
    except Exception as e:
        print(f"❌ Failed: {e}")
        print("\nTry checking your Supabase dashboard for the correct host.")

asyncio.run(test_connection())