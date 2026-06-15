# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Setup**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Run dev server**
```bash
uvicorn app.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs` after starting.

**Docker**
```bash
docker build -t resort-vip-admin-api .
docker run -p 8000:8000 --env-file .env resort-vip-admin-api
```

## Environment

Create a `.env` file at the project root (see `.env.example`):

```env
APP_NAME=Resort VIP Admin API
APP_ENV=local

DB_SERVER=localhost
DB_NAME=ResortVipAdminDB
DB_USER=resortmgr
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 18 for SQL Server

FRONTEND_ORIGIN=http://localhost:5173
VIP_FRONTEND_URL=http://localhost:5174

JWT_SECRET_KEY=change_this_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Embedding (Azure OpenAI only)
EMBEDDING_PROVIDER=azure
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# AI provider: azure | lmstudio | gemini | ollama
AI_PROVIDER=azure

# Azure OpenAI (used for both LLM and embeddings)
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_BASE_URL=
AZURE_OPENAI_DEPLOYMENT_NAME=

LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL_NAME=

GEMINI_API_KEY=
GEMINI_MODEL_NAME=gemini-3.5-flash

OLLAMA_MODEL_NAME=
OLLAMA_BASE_URL=http://localhost:11434

# Qdrant Cloud (vector store for RAG)
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=
```

## Architecture

**Stack:** Python 3.12 · FastAPI · SQL Server (PyODBC + SQLAlchemy 2.0) · JWT (python-jose) · bcrypt (passlib) · LangChain · Qdrant Cloud

**Layer structure:** each domain follows `router → service → model/schema`.

- [app/main.py](app/main.py) — FastAPI app, CORS middleware, router registration under `/api/*`
- [app/config.py](app/config.py) — `Settings` singleton loaded from `.env` via `python-dotenv`; all `os.getenv()` calls must go through this class, not be scattered in other modules
- [app/database.py](app/database.py) — SQLAlchemy engine + `SessionLocal` + `get_db` dependency; connects via `mssql+pyodbc://` with a raw ODBC connection string
- [app/dependencies/auth_dependency.py](app/dependencies/auth_dependency.py) — `get_current_user` FastAPI dependency; decodes the Bearer JWT and returns the payload dict

**Auth flow:** `POST /api/auth/login` accepts `{email, password}`, looks up `dbo.Employees` by email, verifies bcrypt hash, returns a JWT containing `sub` (email), `employee_id`, and `role`. All non-auth routes use `Depends(get_current_user)`.

**Database conventions:**
- Schema is managed externally — no ORM migrations, no `Base.metadata.create_all`.
- DB column names are PascalCase (`EmployeeId`); Python model attributes are snake_case (`employee_id`). Map with `mapped_column("EmployeeId", ...)`.
- For complex or raw queries (e.g. `ItineraryRecommendationService`), use `db.execute(text(...))` with named parameters. Use `.mappings().first()` / `.mappings().all()` to get dict-like rows.

## AI Provider Layer

`app/ai/` contains a pluggable LLM abstraction. The active provider is chosen at runtime by `AI_PROVIDER` in `.env`.

- [app/ai/base.py](app/ai/base.py) — `BaseAILangchain` ABC; exposes `chat(system_prompt, user_prompt) → str` and `invoke(prompt) → str`. Add new providers by subclassing this.
- [app/ai/factory.py](app/ai/factory.py) — `create_ai_langchain(ai_type)` factory; reads provider-specific keys from `settings`.
- [app/ai/embedding_factory.py](app/ai/embedding_factory.py) — `get_embedding_function() → Embeddings`; currently supports `azure` only via `OpenAIEmbeddings`.
- Concrete LLM providers: `GeminiLangchain`, `AzureLangchain`, `LMStudioLangchain`, `OllamaLangchain`.

To add a new LLM provider: subclass `BaseAILangchain`, add its `AiType` enum value in [app/enums/ai_type.py](app/enums/ai_type.py), wire it in the factory, and add the required env vars to `config.py`.

## RAG Pipeline

The itinerary recommendation feature uses a Retrieval-Augmented Generation pipeline backed by **Qdrant Cloud**:

1. **VipPromptService** — queries SQL to gather customer profile, booking, and stay notes.
2. **ItineraryKnowledgeService** — connects to a Qdrant Cloud collection via `QdrantVectorStore.from_existing_collection`; runs `similarity_search_with_score` across five time-slot search plans (09:00, 11:00, 13:00, 15:00, 18:00); deduplicates by `place_name` within a day; fetches full item data from `dbo.ResortKnowledgeItem` by `source_file`. Requires `QDRANT_URL`, `QDRANT_API_KEY`, and `QDRANT_COLLECTION_NAME` to be set — the service raises `ValueError` at init if any are missing.
3. **prompt_builder** ([app/prompts/prompt_builder.py](app/prompts/prompt_builder.py)) — assembles the system and user prompts from the retrieved context.
4. **create_ai_langchain** — calls the active LLM provider; response is expected JSON (possibly wrapped in ` ```json ``` ` fences), stripped in `CheckInService.parse_ai_json`.
5. **ItineraryRecommendationService** — persists the parsed result to `dbo.VipItineraryRecommendation` and `dbo.VipItinerarySchedule` via raw SQL.

Embedding uses Azure OpenAI (`EMBEDDING_PROVIDER=azure`). The Qdrant collection must be populated before calling the generate endpoint; there is no local index file — the vector store lives in Qdrant Cloud.

## Adding a New Module

Follow the pattern of the existing modules (e.g. `customer_service_request`):

1. **Model** (`app/models/`) — SQLAlchemy `Base` subclass; map PascalCase columns explicitly.
2. **Schema** (`app/schemas/`) — Pydantic models for request/response; use `ConfigDict(from_attributes=True)` on response schemas.
3. **Service** (`app/services/`) — class taking `db: Session`; all business logic lives here. Export a module-level singleton instance (e.g. `customer_service_request_service = CustomerServiceRequestService()`) so routers can import it directly.
4. **Router** (`app/routers/`) — thin `APIRouter`; imports the singleton service and delegates. Add `Depends(get_current_user)` on every endpoint that requires auth.
5. Register in [app/main.py](app/main.py) with `app.include_router(..., prefix="/api/...", tags=[...])`.
