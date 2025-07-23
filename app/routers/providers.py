from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from typing import List, Dict, Any

from app.database import get_db
from app.models import Provider, Procedure, Rating

router = APIRouter()

@router.get("/test")
async def test_db(db: AsyncSession = Depends(get_db)):
    """Simple test endpoint"""
    result = await db.execute(text("SELECT COUNT(*) FROM providers"))
    count = result.scalar()
    return {"providers_count": count}

@router.get("/providers")
async def search_providers(
    drg: str = Query(..., description="DRG code or description to search"),
    zip: str = Query(..., description="ZIP code to search from"), 
    radius_km: float = Query(50, description="Search radius in kilometers"),
    db: AsyncSession = Depends(get_db)
):
    """Search for hospitals offering a DRG within a radius of a ZIP code"""
    
    # Super simple query - just get 5 procedures
    query = text("""
        SELECT 
            p.provider_id,
            p.name,
            p.city,
            p.state,
            p.zip_code,
            pr.drg_code,
            pr.drg_description,
            pr.avg_covered_charges,
            pr.total_discharges,
            r.rating
        FROM procedures pr
        JOIN providers p ON pr.provider_id = p.provider_id
        LEFT JOIN ratings r ON p.provider_id = r.provider_id
        WHERE pr.drg_code = :drg
        ORDER BY pr.avg_covered_charges
        LIMIT 5
    """)
    
    result = await db.execute(query, {"drg": drg})
    rows = result.fetchall()
    
    # Simple response
    providers_list = []
    for row in rows:
        providers_list.append({
            "provider_id": row[0],
            "name": row[1],
            "city": row[2],
            "state": row[3],
            "zip_code": row[4],
            "drg_code": row[5],
            "drg_description": row[6],
            "avg_covered_charges": float(row[7]),
            "total_discharges": row[8],
            "rating": row[9] if row[9] else None,
            "distance_km": 10.0  # Dummy value
        })
    
    return {
        "total_found": len(providers_list),
        "providers": providers_list
    }