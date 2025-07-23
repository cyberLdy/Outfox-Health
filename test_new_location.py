from app.utils.location import get_zip_coordinates, calculate_distance

# Test ZIP lookups
test_zips = ["10001", "10032", "11201", "10451"]

print("Testing ZIP lookups:")
for zip_code in test_zips:
    coords = get_zip_coordinates(zip_code)
    if coords:
        print(f"ZIP {zip_code}: {coords}")
    else:
        print(f"ZIP {zip_code}: NOT FOUND")

print("\nTesting distances:")
print(f"10001 to 10032: {calculate_distance('10001', '10032'):.2f} km")
print(f"10001 to 11201: {calculate_distance('10001', '11201'):.2f} km")