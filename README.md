# 🏥 Healthcare Cost Navigator (MVP)

A fast, async web service that helps patients explore hospital costs and quality ratings for medical procedures (DRG codes). Includes a natural language assistant powered by OpenAI GPT for flexible querying.

---

## 🚀 Features

- 🔍 **Search Hospitals** by DRG procedure, ZIP code, and radius
- 💰 **Compare Costs**: View charges, payments, and discharges
- ⭐ **Provider Ratings**: Mock 1–10 star quality ratings
- 🤖 **AI Assistant**: Ask natural language questions, get grounded SQL-backed answers
- ⚡ **FastAPI + async PostgreSQL** backend

---

## 🧠 AI Assistant Capabilities

Example queries supported:

- 💰 “What’s the cheapest hospital for knee replacement?”
- 🏆 “Which hospitals have the best ratings for DRG 470?”
- 📍 “Show me hospitals near 10001 within 25km”
- ❌ “What’s the capital of France?” → Rejected as out of scope

---

## 📦 Tech Stack

| Component         | Description                          |
|------------------|--------------------------------------|
| Python 3.11       | Core backend logic                   |
| FastAPI           | Async API framework                  |
| async SQLAlchemy  | ORM for PostgreSQL                   |
| Supabase (PostgreSQL) | Cloud database hosting          |
| OpenAI GPT-4o     | LLM for NL→SQL translation           |
| SimpleMaps        | ZIP-to-coordinates static mapping    |
| Docker Compose    | Local dev setup                      |

---

## 🗄️ Database Schema

Three main tables:

- `providers`: Basic hospital info (ID, name, ZIP, etc.)
- `procedures`: DRG procedures + average charges
- `ratings`: Mock star ratings (1–10) for each provider

---

## ⚙️ Setup Instructions

### 1. Clone + Install

```bash
git clone https://github.com/your/repo.git
cd healthcare-cost-navigator
2. Configure Environment
Create a .env file:

env
Copy
Edit
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
OPENAI_API_KEY=your_openai_api_key
3. Load Data
bash
Copy
Edit
pip install -r requirements.txt
python etl.py
4. Run Server
bash
Copy
Edit
uvicorn app.main:app --reload
Open API docs at: http://localhost:8000/docs

📡 API Endpoints
GET /providers
Search hospitals by DRG + ZIP + radius.

Params:

drg (required): DRG code or description (e.g. 470 or "knee replacement")

zip (required): US ZIP code

radius_km (required): Distance in kilometers

Example:

bash
Copy
Edit
curl "http://localhost:8000/providers?drg=470&zip=10001&radius_km=30"
POST /ask
Ask natural language questions.

Body:

json
Copy
Edit
{ "question": "Which hospitals have best ratings for hip replacement?" }
Example:

bash
Copy
Edit
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Top 3 cheapest hospitals for DRG 23"}'
🧪 Example Prompts
Prompt	Response Type
Cheapest hospital for knee replacement	Cost-based ranking
Best hospitals in NY with DRG 291	Quality-based ranking
Hospitals within 25km of 10001 for DRG 470	Geo + procedure
Total number of DRG 470 discharges in NYC hospitals	Aggregation query
What's the capital of France?	❌ Out of scope

📌 Reflections on LLMs + SQL
This project shows how LLMs + structured data enable natural language analytics with:

✅ DRG codes, ZIPs, costs → Easy to map to SQL
✅ Schema-aware prompting ensures accuracy
✅ GPT-4o handles most questions well without RAG

But real-world healthcare often involves unstructured data (PDFs, EHR notes, etc.). These require:

🔎 RAG pipelines (Retrieval-Augmented Generation)

🧠 Vector DBs (e.g. FAISS, Chroma) for semantic search

🔍 NLP-based data normalization

🚀 Future Ideas
Feature	Description
🔍 Fuzzy DRG Search	Handle typo'd descriptions like "knee replace" → DRG 470
📍 Natural Language Geo	Support "near Brooklyn" → ZIP code mapping
📊 Chart-Friendly Output	JSON schema for frontend visualizations
⚡ Query Caching	Speed up common question responses
🧠 AI Intent Routing	Detect cost vs. rating vs. volume queries

📚 Data Sources
CMS Medicare Inpatient Charges (NY sample)

SimpleMaps ZIP Database (Free)

Star ratings: Randomized mock data

🖥️ Deployment (Optional)
Use Docker Compose for local deployment:

bash
Copy
Edit
docker-compose up --build
📄 License
MIT License. See LICENSE file.

🙋‍♂️ Author
Built by Dongyu Lin for the Outfox Health Founding Engineer Challenge.