🏥 Healthcare Cost Navigator – MVP Walkthrough
🩺 Part 1: Building /providers API — Structured Hospital Search
✅ Goal
Support the API:

bash
Copy
Edit
GET /providers?drg=470&zip=10001&radius_km=40
→ Return a list of hospitals performing the specified DRG procedure within a ZIP code radius, sorted by cost.

🔍 Problem Breakdown
Parameters

drg: Diagnosis-Related Group code (e.g., 470 = knee replacement)

zip: ZIP code to center the search

radius_km: Radius in kilometers for filtering

Desired Output

Hospitals that perform the given DRG

Must be within the input ZIP code’s radius

Sorted by average_covered_charges (ascending)

🧱 Database Schema
1. providers table
(Hospital metadata from CSV)

provider_id (Rndrng_Prvdr_CCN)

name, city, state, zip_code

lat, lon (added from ZIP dataset)

2. procedures table
(DRG-level hospital charges)

provider_id (FK)

drg_code, drg_description

total_discharges

average_covered_charges

average_total_payments

average_medicare_payments

🚧 Difficulty: ZIP Radius Filtering
❌ Attempt 1: Nominatim API (via geopy)
Easy to use, but fails under load

❗ HTTP 429 and timeouts → Rejected

❌ Attempt 2: PostGIS
Ideal (native SQL: ST_DistanceSphere)

❗ Not supported on Supabase free tier → Rejected

✅ Final Solution: SimpleMaps ZIP Dataset
Used local CSV of ZIP → (lat, lon)

Added lat/lon to providers table during ETL

Used geopy.distance.geodesic() at runtime

Parallelized with FastAPI + SQLAlchemy + thread pool

🧪 Result
GET /providers?drg=XXX&zip=YYYY&radius_km=ZZZ

Filters hospitals by radius

Sorts by cost (avg_covered_charges)

Fully async + scalable

🤖 Part 2: LLM-Powered Natural Language to SQL (NLSQL)
🎯 Goal
Support queries like:

arduino
Copy
Edit
"What's the cheapest hospital for knee replacement?"
→ Auto-generate SQL
→ Execute on database
→ Return grounded answer

🧠 Prompt + Inference Strategy
Feed natural question to LLM (e.g. GPT-4o)

Prompt tells it:

Schema details

Response format (SQL, Answer)

Backend parses sql_query

Executes it and formats the result

Returns grounded + human-readable response

🧪 Examples & Trials
bash
Copy
Edit
curl -X 'POST' http://localhost:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What'\''s the cheapest hospital for knee replacement?"}'
✅ Generated SQL:

sql
Copy
Edit
SELECT providers.name, providers.city, providers.state, procedures.avg_covered_charges
FROM providers
JOIN procedures ON providers.provider_id = procedures.provider_id
WHERE procedures.drg_code = '470'
ORDER BY procedures.avg_covered_charges
LIMIT 1;
✅ Answer:
"The cheapest hospital is Cambridge Health Alliance in Cambridge, MA with an average covered charge of $17,785.20"

⚠️ Challenge: SQL + Answer Grounding Consistency
LLM sometimes adds LIMIT 1, sometimes not

Some queries return raw SQL, others return raw rows

Need to standardize:

SQL generation pattern

Output formatting logic (top N / summary phrasing)

🌟 Ratings Integration (Part 2.5)
📦 New Data: Hospital_General_Information.csv
Contains CMS star ratings (1–5)

Added ratings table to DB:

provider_id, rating

Joined with providers for richer query support

🤖 Sample Ratings Queries
"Which hospitals have the best ratings for knee replacement?"

"Show me hospitals in NY with ratings above 8"

"Top 5 hospitals for DRG 23 with the highest rating"

✅ Updated Prompt
Includes ratings in schema + examples of SQL joins with:

sql
Copy
Edit
JOIN ratings ON providers.provider_id = ratings.provider_id
🧪 Output Example
json
Copy
Edit
{
  "question": "Show me hospitals in NY with ratings above 8",
  "sql_query": "SELECT p.name, p.city, p.state, r.rating FROM providers p JOIN ratings r ON p.provider_id = r.provider_id WHERE p.state = 'NY' AND r.rating > 8;",
  "answer": "Found 11 results. Top 5 include: Northern Dutchess Hospital, NY-Presbyterian Hospital, etc."
}
🛠️ Future Features (Post-MVP)
Feature	Description
🔍 Fuzzy DRG Search	Map "knee replace" → DRG 470 using keyword-to-code lookup or embeddings
📍 Natural Location	Handle queries like “near LA” or “within 20 mi of 94103” → ZIP radius logic
📊 Chart Output	Return JSON in chart-ready format (e.g. bar chart data) for frontend visual
🧠 RAG for EHR/PDFs	Future extension for unstructured data using retrieval + semantic search

✅ Conclusion
🔹 For structured data, SQL + OpenAI + prompt engineering = ✅ MVP success

🔹 For unstructured data, use RAG, vector DBs, and advanced NLP

🔹 Ratings integration added semantic value without changing infrastructure

