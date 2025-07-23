"""
test_integrations.py - Test all external service integrations
Verifies database, OpenAI API, and geocoding services are properly configured.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from openai import OpenAI

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

print("=" * 60)
print("TESTING EXTERNAL SERVICE INTEGRATIONS")
print("=" * 60)

# 1. TEST DATABASE CONNECTION
async def test_database():
    print("\n1️⃣ DATABASE CONNECTION (Supabase PostgreSQL)")
    print("-" * 60)
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in .env")
        return False
        
    print(f"Connecting to: {DATABASE_URL.split('@')[1].split('/')[0]}...")
    
    try:
        engine = create_async_engine(DATABASE_URL, echo=False)
        
        async with engine.connect() as conn:
            # Test basic connectivity
            await conn.execute(text("SELECT 1"))
            print("✅ Connection successful!")
            
            # Check if tables exist
            result = await conn.execute(text("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('providers', 'procedures', 'ratings')
            """))
            table_count = result.scalar()
            
            if table_count == 3:
                # Get record counts
                providers = await conn.execute(text("SELECT COUNT(*) FROM providers"))
                procedures = await conn.execute(text("SELECT COUNT(*) FROM procedures"))
                ratings = await conn.execute(text("SELECT COUNT(*) FROM ratings"))
                
                print(f"✅ All tables exist!")
                print(f"   - Providers: {providers.scalar():,}")
                print(f"   - Procedures: {procedures.scalar():,}")
                print(f"   - Ratings: {ratings.scalar():,}")
            else:
                print(f"⚠️  Only {table_count}/3 tables found. Run ETL first!")
            
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {type(e).__name__}: {str(e)}")
        return False

# 2. TEST OPENAI API
def test_openai():
    print("\n2️⃣ OPENAI API")
    print("-" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env")
        return False
        
    print(f"Testing API key: {api_key[:8]}...")
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use a model that definitely exists
            messages=[
                {"role": "system", "content": "Reply with exactly: OK"},
                {"role": "user", "content": "Test"}
            ],
            max_tokens=10
        )
        
        print("✅ API Key is valid!")
        print(f"   - Model: {response.model}")
        print(f"   - Usage: {response.usage.total_tokens} tokens")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        return False

# 3. TEST GEOCODING
def test_geocoding():
    print("\n3️⃣ GEOCODING SERVICE (ZIP → Coordinates)")
    print("-" * 60)
    
    try:
        # Import after fixing path
        from app.utils.location import get_zip_coordinates, calculate_distance
        
        # Test sample ZIPs
        test_zips = {"10001": "Manhattan", "11201": "Brooklyn", "10451": "Bronx"}
        success_count = 0
        
        for zip_code, name in test_zips.items():
            coords = get_zip_coordinates(zip_code)
            if coords:
                print(f"✅ {zip_code} ({name}): {coords[0]:.4f}, {coords[1]:.4f}")
                success_count += 1
            else:
                print(f"❌ {zip_code} ({name}): Not found")
        
        # Test distance calculation
        if success_count >= 2:
            dist = calculate_distance("10001", "11201")
            if dist != float('inf'):
                print(f"\n✅ Distance calculation working:")
                print(f"   Manhattan → Brooklyn: {dist:.1f} km ({dist * 0.621371:.1f} miles)")
                return True
                
        return success_count > 0
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("   Make sure you're running from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Geocoding test failed: {str(e)}")
        return False

# 4. RUN ALL TESTS
async def main():
    print("\nRunning all integration tests...\n")
    
    # Track results
    results = {
        "Database": await test_database(),
        "OpenAI API": test_openai(),
        "Geocoding": test_geocoding()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    for service, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {service}: {'PASSED' if status else 'FAILED'}")
    
    all_passed = all(results.values())
    print(f"\n{'🎉 All tests passed! Ready to run the app.' if all_passed else '⚠️  Some tests failed. Check configuration.'}")
    
    return all_passed

if __name__ == "__main__":
    asyncio.run(main())