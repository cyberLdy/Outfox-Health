import requests

queries = [
    {"question": "Who is cheapest for DRG 470 within 25 miles of 10001?"},
    {"question": "Who is cheapest for DRG 480 within 50 miles of 35235?"},
    {"question": "What's the cheapest hospital for knee replacement near me?"},
    {"question": "What's the cheapest hospital for HEART FAILURE AND SHOCK WITH MCC near me?"},
    {"question": "Which hospitals have the best ratings for heart surgery?"},
    {"question": "Who has the best ratings for heart surgery near 10032?"},
    {"question": "What's the weather today?"}, # Out of scope
    {"question": "What's the capital of France?"}  # Out of scope
]

endpoints = [ "http://127.0.0.1:8000/ask"]

for i, q in enumerate(queries, 1):
    print(f"\n===== Test {i}: {q['question']} =====")
    success = False
    for url in endpoints:
        try:
            response = requests.post(url, json=q, timeout=5)
            print(f"[✓] Response from {url}")
            print(response.json())
            success = True
            break
        except requests.exceptions.RequestException as e:
            print(f"[!] Failed to connect to {url}: {e}")
    if not success:
        print("❌ All endpoints failed for this question.")
