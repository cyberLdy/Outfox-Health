import pandas as pd
from geopy.distance import geodesic
import functools

# Load ZIP codes once when module is imported
print("Loading ZIP code database...")
zip_df = pd.read_csv('uszips.csv', encoding='latin-1')
print(f"Loaded {len(zip_df)} ZIP codes")

# Create a dictionary for fast lookup
zip_coords = {}
for _, row in zip_df.iterrows():
    zip_coords[str(row['zip'])] = (row['lat'], row['lng'])

def get_zip_coordinates(zip_code: str):
    """Get latitude and longitude for a ZIP code from our database"""
    return zip_coords.get(zip_code)

def calculate_distance(zip1: str, zip2: str) -> float:
    """Calculate distance in km between two ZIP codes"""
    coords1 = get_zip_coordinates(zip1)
    coords2 = get_zip_coordinates(zip2)
    
    if coords1 and coords2:
        return geodesic(coords1, coords2).kilometers
    
    return float('inf')  # If we can't find one of the ZIPs