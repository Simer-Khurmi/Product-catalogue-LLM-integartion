# Product-catalogue-LLM-integartion
Jio AI Telecom Assistant

AI-powered assistant and demo suite for telecom scenarios that unifies:

Natural language → TM Forum Open API orchestration

Modular client layer for TMF620 (Catalog), TMF622 (Ordering), TMF629 (Customer), TMF635 (Usage), TMF678/682 (Billing)

Multiple frontends: Swagger (for testing), Streamlit Chat UI, and an Advanced Web App (dashboard)

Mock/Live toggling via .env to demo safely or integrate with real endpoints

Table of Contents

Features

Architecture

Repository Structure

Requirements

Quick Start

Configuration

Run

API Reference

Streamlit Chat UI

Advanced Web App

Mock Data

Docker (Optional)

Troubleshooting

Roadmap

License

Features

LLM intent parsing (LangChain + HF): natural language to {action, id, filters} action plans

TMF modules

TMF620 Product Catalog: list/filter offerings, details

TMF622 Product Ordering: basic order/recharge flow

TMF629 Customer: profile and subscriptions

TMF635 Usage: usage summaries

TMF678/682 Billing: last bill and balance

Frontends

Swagger docs via FastAPI

Streamlit chat interface

Advanced Web App (HTML/JS) served by FastAPI at /app

Mock/Live: local MOCK_DATA.json for demos; switch to real TMF endpoints via .env

Architecture

High-level flow:

User interacts via Swagger, Streamlit, or the Web App.

FastAPI gateway validates requests.

LLM connector converts free text to a structured action plan.

TMF clients execute the appropriate API calls (mock or live).

Unified JSON responses return to frontends.

[User (Web App / Streamlit / Swagger)]
                |
           FastAPI /api
                |
         LLM Connector (LangChain+HF)
                |
      ┌─────────┴─────────┐
      │                   │
   TMF620              TMF622 ... (other TMF clients)
 (Catalog)             (Ordering, Customer, Usage, Billing)
                |
        Mock JSON or Live TMF endpoints


You can add an image docs/architecture.png and reference it here.

Repository Structure
.
├── api/
│   ├── main.py                # FastAPI app: APIs + serves /app (web)
│   ├── models.py              # Pydantic schemas
│   ├── llama_connector.py     # LLM (LangChain + HF) -> ActionPlan JSON
│   ├── tmf_client.py          # TMF620 Product Catalog
│   ├── order_client.py        # TMF622 Product Ordering
│   ├── customer_client.py     # TMF629 Customer
│   ├── usage_client.py        # TMF635 Usage
│   ├── billing_client.py      # TMF678/682 Billing
│   ├── settings.py            # .env loader
│   └── MOCK_DATA.json         # Mock data for demos
├── web/
│   └── index.html             # Advanced Web App (dashboard)
├── ui/
│   └── app_ui.py              # Streamlit chat UI (optional)
├── .env.example               # Sample configuration
├── requirements.txt
└── README.md

Requirements

Python 3.11.1 (recommended via pyenv)

pip

(Optional) Docker & Docker Compose

Quick Start
# 1) Use Python 3.11.1
pyenv install 3.11.1
pyenv shell 3.11.1

# 2) Install dependencies
pip install -r requirements.txt
# or
pip install fastapi uvicorn requests python-dotenv transformers sentencepiece langchain huggingface-hub streamlit

Configuration

Create .env in the repo root (copy from .env.example):

TMF_BASE_URL=                 # e.g., http://localhost:8080/tmf-api  (leave empty for mock)
MOCK_MODE=true                # true -> use MOCK_DATA.json; false -> call TMF endpoints
HTTP_TIMEOUT=20
CACHE_TTL=60


Set MOCK_MODE=false and TMF_BASE_URL to enable live mode against real TMF endpoints.

Run
FastAPI (APIs + Web App)

From the repo root:

uvicorn api.main:app --reload --port 8008


Swagger: http://127.0.0.1:8008/docs

Advanced Web App: http://127.0.0.1:8008/app

Streamlit Chat UI (optional)
streamlit run ui/app_ui.py


Chat UI: http://localhost:8501

API Reference
POST /api/query

Natural language → structured action plan → TMF execution (mock/live).

Request

{
  "query": "show prepaid plans under 500"
}


Response (example)

{
  "action": "list_offers",
  "filters": {"category": "prepaid", "price_lte": 500},
  "result": [ ... products ... ]
}


Other example queries:

"details of offer 1002"

"recharge customer cust123 with plan 1001"

"get usage for cust123"

"what is the balance for cust123"

GET /api/products

Catalog helper for the Web App.

Query params

category: prepaid|postpaid|broadband|enterprise

price_lte: integer

price_gte: integer

status: active|inactive

Example

GET /api/products?category=prepaid&price_lte=500

Streamlit Chat UI

The optional Streamlit UI provides a simple chat interface that calls the backend.
Start it with:

streamlit run ui/app_ui.py

Advanced Web App

The dashboard HTML (web/index.html) is served at /app.

It calls these backend endpoints:

POST /api/query for AI intent parsing + actions

GET /api/products for catalog listing/filtering

If you need to adjust the base URL inside the HTML, define:

<script>
  const API_BASE = "http://127.0.0.1:8008/api";
</script>

Mock Data

api/MOCK_DATA.json ships with sample offerings, a sample customer, and an in-file “orders” array for mock ordering flows.
Example (excerpt):

{
  "productOffering": [
    {"id": "1001", "name": "Prepaid 199", "category": "prepaid", "price": 199, "status": "active", "validity": "28d"},
    {"id": "1002", "name": "Prepaid 399", "category": "prepaid", "price": 399, "status": "active", "validity": "56d"}
  ],
  "customers": [
    {"id": "cust123", "name": "Ravi Kumar", "email": "ravi@example.com", "subscriptions": ["1001"] }
  ],
  "orders": []
}

Docker (Optional)
docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir fastapi uvicorn requests python-dotenv transformers sentencepiece langchain huggingface-hub

COPY api ./api
COPY web ./web
COPY .env ./.env

EXPOSE 8008
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8008"]

docker-compose.yml
version: "3.8"
services:
  jio-ai-assistant:
    build: .
    ports:
      - "8008:8008"
    environment:
      - TMF_BASE_URL=${TMF_BASE_URL}
      - MOCK_MODE=${MOCK_MODE}
      - HTTP_TIMEOUT=${HTTP_TIMEOUT}
      - CACHE_TTL=${CACHE_TTL}


Run

docker build -t jio-ai-assistant .
docker run -p 8008:8008 --env-file .env jio-ai-assistant
# or
docker compose up --build

Troubleshooting

Port already in use: change --port 8008 to another free port.

Module not found (models): ensure imports are relative in api/main.py (e.g., from .models import QueryRequest).

uvicorn not found: confirm you’re on Python 3.11.1 env and pip install ran successfully.

CORS: we allow * for local dev. Tighten in production.

Slow LLM: use flan-t5-small and keep max_length modest; consider quantized models for CPU.

Roadmap

Authentication/authorization (API keys / OAuth2)

Production logging & metrics, rate limiting, retries

LoRA/PEFT fine-tuning on Jio intent data

Replace client-side KPI simulation with backend /api/kpi/*

Add more TMF APIs: Trouble Ticketing, Payments, Inventory, Activation

Containerize and add CI/CD, basic canary deploy

License

MIT License. See LICENSE (add one to the repo if you haven’t already).

Maintainers / Credits

Backend: FastAPI + TMF clients

AI: LangChain + HuggingFace (Flan-T5 demo)

Frontends: Swagger, Streamlit chat, HTML dashboard (/app)
