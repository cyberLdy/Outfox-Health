from app.utils.location import get_zip_coordinates, calculate_distance

# Test ZIP codes in New York
test_zips = [
    "10001",  # Manhattan
    "10032",  # Manhattan (Washington Heights)
    "11201",  # Brooklyn
    "10451",  # Bronx
]

print("Testing ZIP code geocoding...")
print("-" * 50)

# Test getting coordinates
for zip_code in test_zips:
    coords = get_zip_coordinates(zip_code)
    if coords:
        print(f"ZIP {zip_code}: Lat={coords[0]:.4f}, Lon={coords[1]:.4f}")
    else:
        print(f"ZIP {zip_code}: Failed to geocode")

print("\nTesting distance calculations...")
print("-" * 50)

# Test distances between ZIP codes
test_pairs = [
    ("10001", "10032"),  # Manhattan to Manhattan
    ("10001", "11201"),  # Manhattan to Brooklyn
    ("10001", "10451"),  # Manhattan to Bronx
]

for zip1, zip2 in test_pairs:
    distance = calculate_distance(zip1, zip2)
    if distance != float('inf'):
        print(f"{zip1} to {zip2}: {distance:.2f} km ({distance * 0.621371:.2f} miles)")
    else:
        print(f"{zip1} to {zip2}: Could not calculate distance")