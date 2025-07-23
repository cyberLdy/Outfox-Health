# Healthcare Cost Navigator (MVP)

A lightweight web service that enables patients to search hospitals offering MS-DRG procedures, compare costs, view quality ratings, and ask questions in natural language.

---

## 🚀 Features

* **Search Hospitals by Procedure**: DRG code or description + ZIP + radius
* **Price Transparency**: Avg. covered charges, total payments, Medicare payments
* **Provider Quality**: Mock star ratings (1-10) for hospitals
* **AI Assistant**: Natural language interface via OpenAI
* **Location-Aware**: Radius filtering using ZIP code coordinates

---

## 🛠 Tech Stack

* Python 3.11, FastAPI (async)
* PostgreSQL (Supabase hosted)
* async SQLAlchemy
* OpenAI (GPT-4o)
* Docker + Docker Compose

---

## ⚙️ Quick Start

### Prerequisites

* Docker + Docker Compose
* Python 3.11+
* Supabase account or local PostgreSQL
* OpenAI API key

### Setup

```bash
# Clone the repo
$ git clone <your-repo-url>
$ cd healthcare-cost-navigator

# Create .env file
$ cp .env.example .env  # Fill in DB + OpenAI keys

# Install Python deps (if not using Docker)
$ pip install -r requirements.txt

# Run ETL script
$ python etl.py

# Start the API
$ uvicorn app.main:app --reload
```

API: [http://localhost:8000](http://localhost:8000)
Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 Endpoints

### GET `/providers`

Search hospitals by DRG code/desc, ZIP code, and radius.

#### Params:

* `drg`: e.g. `470` or `knee`
* `zip`: ZIP code
* `radius_km`: radius in kilometers

#### Example

```bash
curl "http://localhost:8000/providers?drg=470&zip=10001&radius_km=40"
```

#### Response

```json
{
  "total_found": 20,
  "providers": [
    {
      "provider_id": "330160",
      "name": "Staten Island University Hospital",
      "city": "Staten Island",
      "state": "NY",
      "zip_code": "10305",
      "distance_km": 18.41,
      "avg_covered_charges": 58545.5,
      "avg_total_payments": 24447.15,
      "avg_medicare_payments": 16855.06,
      "total_discharges": 34,
      "rating": 10,
      "drg_code": "470",
      "drg_description": "MAJOR HIP AND KNEE JOINT REPLACEMENT..."
    }
  ]
}
```

### POST `/ask`

Ask healthcare-related questions using natural language.

#### Example

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Which hospitals in NY have ratings above 8?"}'
```

#### Response

```json
{
  "answer": "Found 28 results. Here are the top 5: ...",
  "sql_query": "SELECT ..."
}
```

---

## 💬 Sample AI Queries

### ✅ Valid Queries

* What's the cheapest hospital for knee replacement?
* Top 5 cheapest hospitals for DRG 23
* Which hospitals in Brooklyn perform the most hip replacements?
* Show hospitals in NY with ratings above 8
* How many hospitals in NY perform heart surgery?

### ❌ Out-of-Scope Queries

* What's the capital of France?
* Tell me a joke

---

## 🧠 Architecture Decisions

| Area          | Decision                                                           |
| ------------- | ------------------------------------------------------------------ |
| Schema        | Normalized (providers, procedures, ratings)                        |
| Geocoding     | Static ZIP→lat/lon using SimpleMaps CSV                            |
| Radius Filter | Python-based haversine distance (not PostGIS)                      |
| AI Model      | GPT-4o via OpenAI, constrained with grounding & SQL-only responses |
| Async Stack   | Fully async with FastAPI + SQLAlchemy                              |
| Ratings       | Random mock (1-10), joined by provider\_id                         |

---

## 🔮 Future Directions

| Feature               | Description                                                        |
| --------------------- | ------------------------------------------------------------------ |
| 🔍 Fuzzy DRG search   | Map typos or variants like "knee replace" → DRG 470                |
| 📍 NLP for ZIP/radius | Parse phrases like "within 20km of 10001" into filter logic        |
| 📊 Chart API          | Return chart-ready schemas for frontend (e.g. bar/pie comparisons) |
| ⭐ Real Ratings        | Pull actual Medicare star ratings                                  |
| ⚡ Query Caching       | Cache frequent responses (e.g. Redis)                              |
| 🩺 More Procedures    | Ingest more DRG types for broader coverage                         |
| 👤 User Accounts      | Save preferences, searches, bookmarks                              |

---

## 📦 Data Sources

* **Pricing**: CMS Provider Utilization & Payment Data (NY sample)
* **ZIP Codes**: [SimpleMaps US ZIP Code Database](https://simplemaps.com/data/us-zips)
* **Ratings**: Synthetic (1-10), mock-generated

---

## 🪪 License

MIT License - See LICENSE file for full details.
