import requests

queries = [
    {"question": "What's the cheapest hospital for knee replacement?"},
    {"question": "Which hospitals have the best ratings for knee replacement?"},
    {"question": "Show me hospitals in NY with ratings above 8"},
    {"question": "What are the top 5 cheapest hospitals for DRG 23?"},
    {"question": "What's the capital of France?"}  # Out of scope
]

for i, q in enumerate(queries, 1):
    print(f"\n===== Test {i}: {q['question']} =====")
    response = requests.post("http://localhost:8000/ask", json=q)
    print(response.json())
