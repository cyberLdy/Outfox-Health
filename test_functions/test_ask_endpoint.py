import requests

queries = [
    {"question": "What's the cheapest hospital for knee replacement?"},
    {"question": "Which hospitals have the best ratings for knee replacement?"},
    {"question": "Show me hospitals in NY with ratings above 8"},
    {"question": "What are the top 5 cheapest hospitals for DRG 23?"},
    {"question": "What's the capital of France?"}  # Out of scope
]

endpoints = ["http://localhost:8000/ask", "http://127.0.0.1:8000/ask"]

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
