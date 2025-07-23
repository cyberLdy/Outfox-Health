from pydantic import BaseModel
from typing import List, Optional

class ProviderResponse(BaseModel):
    provider_id: str
    name: str
    city: str
    state: str
    zip_code: str
    distance_km: float
    avg_covered_charges: float
    avg_total_payments: float
    avg_medicare_payments: float
    total_discharges: int
    rating: Optional[int]
    drg_code: str
    drg_description: str

class ProviderSearchResponse(BaseModel):
    total_found: int
    providers: List[ProviderResponse]

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sql_query: Optional[str] = None