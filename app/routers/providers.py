from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.database import get_db
from app.models import Provider, Procedure, Rating
from app.schemas import ProviderSearchResponse, ProviderResponse
from app.utils.location import calculate_distance

router = APIRouter()

# Thread pool for blocking geocoding operations
executor = ThreadPoolExecutor(max_workers=3)

async def calculate_distance_async(zip1: str, zip2: str) -> float:
    """Run blocking distance calculation in thread pool"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, calculate_distance, zip1, zip2)

@router.get("/providers", response_model=ProviderSearchResponse)
async def search_providers(
    drg: str = Query(..., description="DRG code or description to search"),
    zip: str = Query(..., description="ZIP code to search from"), 
    radius_km: float = Query(50, description="Search radius in kilometers"),
    db: AsyncSession = Depends(get_db)
):
    """Search for hospitals offering a DRG within a radius of a ZIP code"""
    
    # Build query with joins
    query = select(Procedure, Provider, Rating).join(
        Provider, Procedure.provider_id == Provider.provider_id
    ).outerjoin(
        Rating, Provider.provider_id == Rating.provider_id
    )
    
    # Filter by DRG code or description
    if drg.isdigit():
        query = query.where(Procedure.drg_code == drg)
    else:
        query = query.where(Procedure.drg_description.ilike(f"%{drg}%"))
    
    # Execute query
    result = await db.execute(query)
    rows = result.all()
    
    # Process results with distance calculation
    providers_with_distance = []
    
    # Calculate distances in batches to avoid too many geocoding requests
    for procedure, provider, rating in rows[:100]:  # Limit to first 100 for performance
        try:
            # Calculate distance
            distance = await calculate_distance_async(zip, provider.zip_code)
            
            # Only include if within radius
            if distance <= radius_km:
                providers_with_distance.append({
                    "provider": provider,
                    "procedure": procedure,
                    "rating": rating,
                    "distance": distance
                })
        except Exception as e:
            print(f"Error calculating distance for {provider.zip_code}: {e}")
            continue
    
    # Build response objects
    providers_list = []
    for item in providers_with_distance:
        provider = item["provider"]
        procedure = item["procedure"]
        rating = item["rating"]
        
        providers_list.append(ProviderResponse(
            provider_id=provider.provider_id,
            name=provider.name,
            city=provider.city,
            state=provider.state,
            zip_code=provider.zip_code,
            distance_km=round(item["distance"], 2),
            avg_covered_charges=procedure.avg_covered_charges,
            avg_total_payments=procedure.avg_total_payments,
            avg_medicare_payments=procedure.avg_medicare_payments,
            total_discharges=procedure.total_discharges,
            rating=rating.rating if rating else None,
            drg_code=procedure.drg_code,
            drg_description=procedure.drg_description
        ))
    
    # Sort by average covered charges (cheapest first)
    providers_list.sort(key=lambda x: x.avg_covered_charges)
    
    return ProviderSearchResponse(
        total_found=len(providers_list),
        providers=providers_list
    )

@router.get("/test")
async def test_db(db: AsyncSession = Depends(get_db)):
    """Simple test endpoint"""
    from sqlalchemy import text
    result = await db.execute(text("SELECT COUNT(*) FROM providers"))
    count = result.scalar()
    return {"providers_count": count}