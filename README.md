VIDEO: https://www.loom.com/share/8579fb024ffe407d8ef109ffd9bfdd0f

# 🏥 Healthcare Cost Navigator (MVP)

A fast, async web service that helps patients explore hospital costs and quality ratings for medical procedures (DRG codes). Includes a natural language assistant powered by OpenAI GPT for flexible querying.

---

## 🚀 Features

- 🔍 **Search Hospitals** by DRG procedure, ZIP code, and radius
- 💰 **Compare Costs**: View charges, payments, and discharges
- ⭐ **Real + Mock Ratings**: CMS star ratings (2,059 hospitals) + mock ratings for others
- 🤖 **AI Assistant**: Ask natural language questions, get SQL-backed answers
- ⚡ **FastAPI + async PostgreSQL** backend

---

## 🧠 AI Assistant Capabilities

Example queries supported:

- 💰 "What's the cheapest hospital for knee replacement?"
- 🏆 "Which hospitals have the best ratings for DRG 470?"
- 📍 "Show me hospitals near 10001 within 25km"
- ❌ "What's the capital of France?" → Rejected as out of scope

---

## 📦 Tech Stack

| Component         | Description                          |
|------------------|--------------------------------------|
| Python 3.11       | Core backend logic                   |
| FastAPI           | Async API framework                  |
| async SQLAlchemy  | ORM for PostgreSQL                   |
| Supabase (PostgreSQL) | Cloud database hosting          |
| OpenAI GPT-4o-mini | LLM for NL→SQL translation         |
| SimpleMaps        | ZIP-to-coordinates static mapping    |
| Docker Compose    | Local dev setup                      |

---

## 🗄️ Database Schema

Three main tables:

- `providers`: Basic hospital info (ID, name, ZIP, etc.)
- `procedures`: DRG procedures + average charges
- `ratings`: Real CMS star ratings (1-5 → 2-10 scale) + mock ratings

---

## ⚙️ Setup Instructions

### 1. Clone + Install

```bash
git clone https://github.com/your/repo.git
cd healthcare-cost-navigator
2. Configure Environment
Create a .env file:
envDATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
OPENAI_API_KEY=your_openai_api_key
3. Prepare Data Files
Ensure these files are in the dataset/ folder:

MUP_INP_RY24_P03_V10_DY22_PrvSvc.csv - Hospital pricing data
Hospital_General_Information.csv - CMS star ratings ✨
uszips.csv - ZIP code coordinates

4. Load Data
bashpip install -r requirements.txt
python etl.py
5. Run Server
bashuvicorn app.main:app --reload
Open API docs at: http://localhost:8000/docs

📡 API Endpoints
GET /providers
Search hospitals by DRG + ZIP + radius.
Params:

drg (required): DRG code or description (e.g. 470 or "knee replacement")
zip (required): US ZIP code
radius_km (default: 50): Distance in kilometers

Example:
bashcurl "http://localhost:8000/providers?drg=470&zip=10001&radius_km=30"
POST /ask
Ask natural language questions.
Body:
json{ "question": "Which hospitals have best ratings for hip replacement?" }
Example:
bashcurl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Top 3 cheapest hospitals for DRG 23"}'

🧪 Testing Suite
The test_functions/ folder contains comprehensive tests:

verify_datasets.py - Validates all CSV files are present and readable
test_integrations.py - Tests database, OpenAI API, and geocoding services
test_api_endpoints.py - End-to-end API testing with sample queries

Run all tests:
bashpython test_functions/verify_datasets.py
python test_functions/test_integrations.py  # Ensure services are configured
python test_functions/test_api_endpoints.py  # Server must be running

🧠 Implementation Challenges
⚠️ Challenge 1: ZIP Radius Filtering
Problem: Need to filter hospitals within a radius of any ZIP code.
Attempted Solutions:

❌ Nominatim API: Rate limited (HTTP 429), unreliable for production
❌ PostGIS: Perfect but not available on Supabase free tier
✅ SimpleMaps Dataset: Offline ZIP→lat/lon mapping (96.4% coverage)

Result: 2,681 out of 2,782 hospital ZIPs can be geocoded. Missing ~100 ZIPs are filtered out gracefully.
⚠️ Challenge 2: LLM Response Consistency
Problem: GPT sometimes added LIMIT 1, sometimes didn't. Inconsistent formatting.
Solution:

Enhanced prompts with explicit SQL rules
Smart answer formatting based on query intent
Fallback handling for out-of-scope questions


📊 Data Sources

Hospital Pricing: CMS Medicare Provider Utilization (15k NY records)
ZIP Coordinates: SimpleMaps US ZIP Database (33k ZIPs)
Star Ratings: CMS Hospital Compare (2,059 real ratings) ✨

Real ratings: 68.3% of hospitals
Mock ratings: 31.7% (generated 4-9 scale)




🏆 Bonus Features Implemented
✅ Real Hospital Quality Ratings: Integrated actual CMS star ratings

Matched 2,059 hospitals with official CMS ratings
Converted 1-5 star scale to 2-10 for better granularity
Only 956 hospitals use mock ratings (those not in CMS data)


📌 Reflections on LLMs + Healthcare Data
What Works Well (Structured Data)

✅ Tabular data (CSV) → SQL queries via LLM
✅ Clear schema enables reliable NL→SQL translation
✅ Grounded responses prevent hallucination

Real-World Challenges (Unstructured Data)
Healthcare often involves:

📄 PDFs, clinical notes, discharge summaries
🏥 EHR free-text fields
📋 Medical guidelines and protocols

These require:

🔎 RAG pipelines for context grounding
🧠 Vector databases for semantic search
🔍 Advanced NLP for medical language understanding


🚀 Future Improvement Ideas
FeatureDescription🔍 Fuzzy DRG SearchHandle typos like "knee replacmnt" → DRG 470📍 Natural Language GeoSupport "near Brooklyn" → ZIP code mapping📊 Chart-Ready OutputReturn visualization-friendly JSON⚡ Query CachingSpeed up repeated questions🧠 Intent ClassificationRoute cost vs. quality vs. location queries

🖥️ Deployment (Optional)
Use Docker Compose for local deployment:
bashdocker compose up --build

📚 Additional Documentation
For deeper technical insights:

difficulty.md - Deep dive on ZIP radius filtering challenge
ideas.md - Reflections on LLM vs RAG for healthcare data
mvp_walkthrough.md - Step-by-step implementation journey


📄 License
MIT License. See LICENSE file.

🙋‍♂️ Author
Built by Dongyu Lin for the Outfox Health Founding Engineer Challenge.

