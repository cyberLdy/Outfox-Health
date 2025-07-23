# test_providers_endpoint.py

import requests

BASE_URL = "http://localhost:8000"

tests = [
    {
        "desc": "DRG code only (470 - knee replacement)",
        "params": {"drg": "470", "zip": "10001", "radius_km": "50"}
    },
    {
        "desc": "DRG keyword search (fuzzy matching: 'knee replace')",
        "params": {"drg": "knee replace", "zip": "10001", "radius_km": "50"}
    },
    {
        "desc": "Invalid ZIP code",
        "params": {"drg": "470", "zip": "99999", "radius_km": "50"}
    },
    {
        "desc": "No radius provided",
        "params": {"drg": "470", "zip": "10001"}
    },
    {
        "desc": "Out-of-range ZIP",
        "params": {"drg": "470", "zip": "90210", "radius_km": "10"}
    }
]

for i, test in enumerate(tests, 1):
    print(f"\n===== Test {i}: {test['desc']} =====")
    try:
        response = requests.get(f"{BASE_URL}/providers", params=test["params"])
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(response.json())
    except Exception as e:
        print(f"Request failed: {e}")
