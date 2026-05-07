# Expense Tracker API

Lightweight backend API for tracking expenses, categories, and budgets. Built with FastAPI and SQLAlchemy.

## Features
- User authentication (JWT)
- CRUD for categories, expenses, budgets
- Simple reporting endpoints

## Project structure

See the repository root for modules: `main.py`, `database.py`, `models/`, `schemas/`, `routes/`, and `auth/` utilities.

## Requirements
- Python 3.10+
- Install dependencies:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Environment variables
Create a `.env` file in the project root and set at minimum:

- `DATABASE_URL` — SQLAlchemy database URL (e.g. `sqlite:///./dev.db` or a Postgres URL)
- `SECRET_KEY` — JWT signing key
- `ALGORITHM` — JWT algorithm (e.g. `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — token expiry in minutes

## Run the app

Start the development server:

```bash
uvicorn main:app --reload
```

The app runs on `http://127.0.0.1:8000` by default and creates tables automatically using `Base.metadata.create_all(bind=engine)` in `main.py`.

## Models & relationships (overview)

- `User` (`users` table) — `id` is an `Integer` primary key.
- `Categories` (`categories` table) — has `user_id` as an `Integer` foreign key referencing `users.id`.
- Relationship: one `User` -> many `Categories` using SQLAlchemy `relationship(..., back_populates=...)`.

Other models (expenses, budgets) follow the same pattern: a foreign key column referencing `users.id` and ORM relationships for convenient access.

## API routes (high level)

- `routes/auth.py` — signup/login and JWT token endpoints
- `routes/categories.py` — create/list/update/delete categories
- `routes/expenses.py` — manage expenses
- `routes/budget.py` / `routes/budgets.py` — manage budgets (file may vary)
- `routes/reports.py` — reporting endpoints

Refer to the specific route files for exact request/response schemas and payload fields.

## Example usage

1. Create a user (example payload depends on your `routes/auth` implementation).
2. Authenticate to obtain a JWT access token.
3. Use the token to create categories and expenses via the `Authorization: Bearer <token>` header.

## Notes
- Make sure column types match for foreign keys (e.g. `user_id` should be the same type as `users.id`).
- If you switch DB backends, update `DATABASE_URL` accordingly and recreate/migrate the DB.

---
