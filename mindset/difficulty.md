🧠 Implementation Challenges
⚠️ Difficulty 1: ZIP Radius Filtering for /providers
🧩 The Problem
To support filtering hospitals within a radius of a ZIP code, we needed to convert ZIP codes into latitude/longitude and perform distance calculations.

❌ Attempt 1: Nominatim API
Used geopy + Nominatim for geocoding

Issues: Hit HTTP 429 Too Many Requests, even with backoff

❌ Rejected for being unreliable under load and not usable during ETL or live filtering

❌ Attempt 2: PostGIS (e.g. ST_DistanceSphere)
Perfect for SQL-native geospatial queries

Issue: Not supported in [Supabase free tier]

❌ Rejected due to platform constraints

✅ Final Solution: SimpleMaps ZIP Dataset + geopy
Used uszips.csv to map ZIP → (lat, lon)

Stored coordinates in the providers table during ETL

Used Python's geopy.distance.geodesic() during query time to filter results within radius_km

✅ Verification Snapshot
bash
Copy
Edit
Hospital ZIPs we can geocode: 2,681 / 2,782 → 96.4% coverage
For MVP, this is sufficient. In the future, we can fallback to live APIs for the ~100 missing ZIPs.

🔁 Trade-off Table
Method	Pros	Cons
Nominatim	Easy to use	Rate limited, flaky, no batch
PostGIS	Built-in, performant	Not available on Supabase
SimpleMaps ✅	Offline, fast, reliable	Requires preprocessing; some gaps

⚠️ Difficulty 2: Response Grounding + Prompt Formatting for /ask
🧩 The Problem
Initial LLM responses had inconsistent logic:

Sometimes used LIMIT 1, sometimes not

Returned long SQL without meaningful summarization

Inconsistent formatting and fallback logic

🔄 Fixes Implemented
Improved grounding prompt to always generate SQL consistent with intent (e.g. LIMIT 1 if asked for cheapest)

Added better answer formatting and fallback responses

Added timeout fallback to try 127.0.0.1 if localhost fails

✅ Final Sample Logs
bash
Copy
Edit
===== Test 1: What's the cheapest hospital for knee replacement? =====
✓ Response from 127.0.0.1
→ Cambridge Health Alliance (Cambridge, MA), avg charge: $17,785.20
→ SQL: SELECT ... WHERE drg_code = '470' ORDER BY avg_covered_charges LIMIT 1;

===== Test 2: Which hospitals have the best ratings for knee replacement? =====
✓ Prisma Health Patewood Hospital (Greenville, SC), rating: 10/10
→ SQL: SELECT ... ORDER BY ratings.rating DESC;

===== Test 3: Show me hospitals in NY with ratings above 8 =====
✓ Top 5 hospitals in NY, ratings > 8
→ SQL: WHERE state = 'NY' AND rating > 8;

===== Test 4: Top 5 cheapest hospitals for DRG 23 =====
✓ Shows sorted hospitals with charge values
→ SQL: WHERE drg_code = '23' ORDER BY avg_covered_charges LIMIT 5;

===== Test 5: What's the capital of France? =====
✓ Fallback handled: “I can only help with hospital pricing and quality information.”
→ SQL: None
✅ Result
Consistent SQL generation grounded in schema

Robust NL→SQL conversion

Clean formatted answers with fallback for off-topic queries