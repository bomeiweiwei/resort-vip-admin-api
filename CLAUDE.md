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

**API docs** available at `http://localhost:8000/docs` after starting.

## Environment

Create a `.env` file at the project root:

```env
APP_NAME=Resort VIP Admin API
APP_ENV=local

DB_SERVER=localhost
DB_NAME=ResortVipAdminDB
DB_USER=resortmgr
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 17 for SQL Server

FRONTEND_ORIGIN=http://localhost:5173

JWT_SECRET_KEY=change_this_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Architecture

**Stack:** Python 3.12 · FastAPI · SQL Server (via PyODBC + SQLAlchemy 2.0) · JWT (python-jose) · bcrypt (passlib)

**Layer structure:** each domain follows `router → service → model/schema`.

- [app/main.py](app/main.py) — FastAPI app, CORS middleware, router registration under `/api/*`
- [app/config.py](app/config.py) — `Settings` singleton loaded from `.env` via `python-dotenv`
- [app/database.py](app/database.py) — SQLAlchemy engine + `SessionLocal` + `get_db` dependency; connects to MSSQL using a raw ODBC connection string via `mssql+pyodbc://`

**Auth flow:** `POST /api/auth/login` accepts `{email, password}`, looks up `dbo.Employees` by email, verifies bcrypt hash, returns a JWT containing `sub` (email), `employee_id`, and `role`.

**Database:** SQL Server table `dbo.Employees` — no ORM migrations; schema is managed externally. Column names in the DB use PascalCase (`EmployeeId`), mapped to snake_case Python attributes in [app/models/employee_model.py](app/models/employee_model.py).

## Adding a New Module

Follow the pattern of the existing `employee` module:

1. **Model** (`app/models/`) — SQLAlchemy `Base` subclass mapping to the DB table
2. **Schema** (`app/schemas/`) — Pydantic models for request/response; use `ConfigDict(from_attributes=True)` on response schemas
3. **Service** (`app/services/`) — class taking `db: Session`; contains all business logic
4. **Router** (`app/routers/`) — thin `APIRouter`; instantiates the service and delegates
5. Register in [app/main.py](app/main.py) with `app.include_router(..., prefix="/api/...", tags=[...])`
