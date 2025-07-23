from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import functools
import time

# Cache for ZIP code coordinates
zip_cache = {}

@functools.lru_cache(maxsize=1000)
def get_zip_coordinates(zip_code: str):
    """Get latitude and longitude for a ZIP code"""
    if zip_code in zip_cache:
        return zip_cache[zip_code]
    
    try:
        geolocator = Nominatim(user_agent="healthcare-navigator")
        location = geolocator.geocode(f"{zip_code}, USA")
        
        if location:
            coords = (location.latitude, location.longitude)
            zip_cache[zip_code] = coords
            time.sleep(1)  # Be nice to the free geocoding service
            return coords
    except Exception as e:
        print(f"Error geocoding {zip_code}: {e}")
    
    return None

def calculate_distance(zip1: str, zip2: str) -> float:
    """Calculate distance in km between two ZIP codes"""
    coords1 = get_zip_coordinates(zip1)
    coords2 = get_zip_coordinates(zip2)
    
    if coords1 and coords2:
        return geodesic(coords1, coords2).kilometers
    
    return float('inf')  # If we can't calculate, return infinite distance