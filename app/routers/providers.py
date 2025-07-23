from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import Provider, Procedure, Rating
from app.schemas import ProviderSearchResponse, ProviderResponse
from app.utils.location import calculate_distance

router = APIRouter()

@router.get("/providers", response_model=ProviderSearchResponse)
async def search_providers(
    drg: str = Query(..., description="DRG code or description to search"),
    zip: str = Query(..., description="ZIP code to search from"), 
    radius_km: float = Query(50, description="Search radius in kilometers"),
    db: AsyncSession = Depends(get_db)
):
    """Search for hospitals offering a DRG within a radius of a ZIP code"""
    
    # Build query
    query = select(Procedure, Provider, Rating).join(
        Provider, Procedure.provider_id == Provider.provider_id
    ).outerjoin(
        Rating, Provider.provider_id == Rating.provider_id
    )
    
    # Filter by DRG
    if drg.isdigit():
        query = query.where(Procedure.drg_code == drg)
    else:
        query = query.where(Procedure.drg_description.ilike(f"%{drg}%"))
    
    # Execute query
    result = await db.execute(query)
    rows = result.all()
    
    # Filter by distance
    providers_list = []
    for procedure, provider, rating in rows:
        # Calculate real distance
        distance = calculate_distance(zip, provider.zip_code)
        
        # Only include if within radius
        if distance <= radius_km:
            providers_list.append(ProviderResponse(
                provider_id=provider.provider_id,
                name=provider.name,
                city=provider.city,
                state=provider.state,
                zip_code=provider.zip_code,
                distance_km=round(distance, 2),
                avg_covered_charges=procedure.avg_covered_charges,
                avg_total_payments=procedure.avg_total_payments,
                avg_medicare_payments=procedure.avg_medicare_payments,
                total_discharges=procedure.total_discharges,
                rating=rating.rating if rating else None,
                drg_code=procedure.drg_code,
                drg_description=procedure.drg_description
            ))
    
    # Sort by price (cheapest first)
    providers_list.sort(key=lambda x: x.avg_covered_charges)
    
    return ProviderSearchResponse(
        total_found=len(providers_list),
        providers=providers_list
    )