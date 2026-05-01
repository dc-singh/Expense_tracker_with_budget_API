# Expense Tracker API

Comprehensive documentation for the Expense Tracker API project. This README explains how to set up, configure, run, and extend the project from start to finish.

---

**Contents**

- Project overview
- Tech stack
- Prerequisites
- Setup (Windows)
- Environment variables
- Database (PostgreSQL) setup and connection
- Creating database tables
- Running the application
- API summary (existing endpoints)
- Project structure
- Contributing, testing, and deployment
- Troubleshooting & FAQ

---

**Project Overview**

This repository implements a backend API for an Expense Tracker. It provides user management, expense, category, and budget models (some files are scaffolds). The app is written with FastAPI and SQLAlchemy and uses environment variables to configure the PostgreSQL connection.

**Tech stack**

- Python 3.10+ (recommended)
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- PostgreSQL (database)
- python-dotenv (load .env files)

---

**Prerequisites**

- Install Python 3.10+ from python.org
- Install PostgreSQL (locally or use a hosted provider)
- Optional but recommended: Git

---

**Setup (Windows)**

1. Clone the repo and change directory:

```powershell
git clone <repo-url> expense-tracker-api
cd expense-tracker-api
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies (recommended list):

```powershell
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

Later you can freeze these into `requirements.txt`:

```powershell
pip freeze > requirements.txt
```

---

**Environment variables**

Create a `.env` file in the project root (do NOT commit this file).

Example `.env`:

```
DATABASE_URL=postgresql://<DB_USER>:<DB_PASSWORD>@localhost:5432/expense_tracker
```

Replace `<DB_USER>`, `<DB_PASSWORD>`, host, port and database name to match your Postgres setup.

Notes:
- The project reads `DATABASE_URL` using `python-dotenv` and `os.getenv` in `database.py`.
- On Windows you may also set environment variables via system settings or PowerShell session.

---

**Database setup: create the database**

1. Create the physical database in PostgreSQL (example using `createdb`):

```powershell
createdb -U postgres expense_tracker
```

or using psql:

```sql
CREATE DATABASE expense_tracker;
```

2. Put the matching `DATABASE_URL` into your `.env`.

---

**Database connection and `database.py` explanation**

The project uses synchronous SQLAlchemy sessions. Open [database.py](database.py#L1) to inspect the code. Below is the canonical content and a line-by-line explanation.

`database.py` (current file)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv


load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Line-by-line explanation (concise):

- `from sqlalchemy import create_engine` — imports the factory to create a DB engine (sync).
- `from sqlalchemy.orm import sessionmaker, declarative_base` — `sessionmaker` builds session factories; `declarative_base` is used by model classes to register metadata.
- `import os` — used to read environment variables.
- `from dotenv import load_dotenv` — loads `.env` file into the process environment.
- `load_dotenv()` — reads `.env` from project root and sets values in `os.environ`.
- `Base = declarative_base()` — root class for SQLAlchemy models; models inherit from `Base`.
- `DATABASE_URL = os.getenv("DATABASE_URL")` — reads the connection string from environment.
- `engine = create_engine(DATABASE_URL)` — creates a synchronous SQLAlchemy engine using the URL.
- `SessionLocal = sessionmaker(...)` — configures a session factory bound to the engine.
- `def get_db(): ...` — dependency generator used with FastAPI's `Depends` to provide a DB session per request and ensure it is closed afterwards.

How to form the `DATABASE_URL` string

- Typical format (psycopg2 driver):

```
postgresql://username:password@host:port/dbname
```

Examples:

```
postgresql://postgres:secret@localhost:5432/expense_tracker
```

If you prefer async SQLAlchemy (`asyncpg`), I can provide a ready code sample and walk you through converting endpoints to async.

---

**Create database tables from models**

Because this project uses SQLAlchemy models and `Base`, you can create tables with a small Python one-liner (after `DATABASE_URL` is set):

```powershell
python - <<'PY'
from database import Base, engine
Base.metadata.create_all(bind=engine)
print('Tables created')
PY
```

This inspects all `Base` subclasses (your models) and creates tables in the configured database.

For production or controlled migrations, use Alembic — I can add Alembic configuration if you want.

---

**Run the application**

Start the server locally with Uvicorn (development):

```powershell
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to see automatic API docs generated by FastAPI.

---

**Existing endpoints (current project)**

The app contains a minimal `main.py` with two routes:

- `GET /` — returns a welcome message.
- `GET /DBConnection` — demonstrates DB dependency; returns a success message when `get_db` yields a session.

As the `routes/` folder contains scaffolded files, add routers and include them in `main.py` to expose more endpoints. Example pattern in `main.py`:

```python
from fastapi import FastAPI
from routes import expenses, categories

app = FastAPI()
app.include_router(expenses.router)
app.include_router(categories.router)
```

When you build a router file, define an `APIRouter()` and export it as `router`.

---

**Project structure**

Current layout (top-level files and directories):

- `main.py` — FastAPI app and simple routes ([main.py](main.py#L1)).
- `database.py` — SQLAlchemy engine, `SessionLocal`, `Base` and `get_db` dependency ([database.py](database.py#L1)).
- `models/` — SQLAlchemy model classes (e.g., `models/user.py`).
- `schemas/` — Pydantic schemas for request/response validation.
- `routes/` — FastAPI routers (scaffolded).
- `auth/` — authentication helpers (JWT, password hashing) scaffolds.
- `.env` — environment variables (should be created locally, not committed)

Files to check and extend:

- Implement `models/expense.py`, `models/category.py`, `models/budget.py` (scaffolds present).
- Fill in `routes/*` with route logic; use `get_db` for DB access.

---

**Testing**

1. Add tests under a `tests/` directory.
2. Use `pytest` and `httpx`/`asyncio` test clients for FastAPI.
3. For DB tests, use a separate test database or use transaction rollbacks.

Example install:

```powershell
pip install pytest httpx
```

---

**Migrations (recommended)**

For schema evolution, use Alembic. Basic steps:

```powershell
pip install alembic
alembic init alembic
# configure alembic.ini to use DATABASE_URL
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

I can scaffold Alembic configuration for you if you want.

---

**Deployment**

- For production, use a process manager (gunicorn + uvicorn workers, or uvicorn directly with systemd) and an external PostgreSQL instance.
- Set environment variables securely in your hosting environment.

---

**Contributing**

- Follow the existing code style: standard Python with clear function names.
- Add tests for new features.
- Keep secrets out of the repo; use `.env` or platform-specific secret stores.

---

**Troubleshooting & FAQ**

- Q: `create_engine` fails with `None`-type DATABASE_URL — A: Ensure `.env` exists and `DATABASE_URL` is set, or set it in the environment before running.
- Q: I get `psycopg2` installation errors — A: Use `psycopg2-binary` on development machines; on Windows ensure build tools are present or install prebuilt binaries.

---

If you want, I can now:

- (A) Fill the missing model and schema files (`expense`, `category`, `budget`) and implement basic CRUD routes, or
- (B) Add Alembic migrations and `requirements.txt`, or
- (C) Convert the project to async SQLAlchemy and show the async `database.py` version.

Tell me which follow-up task you prefer and I'll proceed.
