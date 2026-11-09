# JobTrack API

A REST API built with FastAPI to track job and internship applications.

## Tech Stack

- Python
- FastAPI
- Uvicorn (server)
- PostgreSQL (database)
- SQLAlchemy (ORM) with psycopg 3 (driver)
- pydantic-settings (reads `.env`)
- Alembic (database migrations)
- Git & GitHub

## Endpoints

| Method | Path      | Description                          |
|--------|-----------|--------------------------------------|
| GET    | `/`       | Confirms the API is running          |
| GET    | `/health` | Health check                         |
| GET    | `/about`  | Developer name, purpose, and skills  |

### Applications (stored in PostgreSQL)

| Method | Path                    | Description                              | Success | Errors   |
|--------|-------------------------|------------------------------------------|---------|----------|
| POST   | `/applications`         | Create an application                    | 201     | 422      |
| GET    | `/applications`         | List all applications                    | 200     | -        |
| GET    | `/applications/{id}`    | Get one application                      | 200     | 404      |
| PUT    | `/applications/{id}`    | Update only the fields you send          | 200     | 404, 422 |
| DELETE | `/applications/{id}`    | Delete an application                    | 204     | 404      |

`status` must be one of: `Applied`, `Interview`, `Offer`, `Rejected`.
`job_link` is optional (max 500 characters).

## Project Structure

```
.env.example           # Template for your private .env (never commit .env)
alembic.ini            # Alembic settings (no password here)
alembic/
  env.py               # Connects Alembic to our settings and models
  versions/            # One file per migration (database change)
app/
  __init__.py
  main.py              # FastAPI app, /, /health, /about
  config.py            # Reads DATABASE_URL from .env
  database.py          # Engine, SessionLocal, Base, get_db
  models.py            # SQLAlchemy "applications" table
  schemas.py           # Pydantic models
  routers/
    __init__.py
    applications.py    # CRUD endpoints
```

## Database Setup (PostgreSQL)

1. Install PostgreSQL and remember the password you set for the `postgres` user.
2. Create the database (in pgAdmin: right-click Databases -> Create -> Database -> name it `jobtrack`), or run:

```powershell
psql -U postgres -c "CREATE DATABASE jobtrack;"
```

3. Create your private `.env` from the template and put your real password in it:

```powershell
copy .env.example .env
```

```
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/jobtrack
```

`.env` is ignored by Git, so your password is never uploaded. If your password has special characters (`@`, `/`, `#`), URL-encode them (`@` becomes `%40`).

The tables are created by Alembic migrations (see step 4 below), not by the app itself.

## How to Run (Windows)

```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database tables (needed before the first run)
alembic upgrade head

# 5. Start the server
uvicorn app.main:app --reload --reload-dir app --port 8001
```

Then open:

- http://127.0.0.1:8001/
- http://127.0.0.1:8001/health
- http://127.0.0.1:8001/about
- http://127.0.0.1:8001/docs (interactive API docs)

## Database migrations

Alembic keeps a history of every change to the database structure, so changes can be applied, undone and shared through Git. Only Alembic changes the tables. The app never does.

| Command | What it does |
|---------|--------------|
| `alembic upgrade head` | Apply all new migrations (run this after pulling new code) |
| `alembic downgrade -1` | Undo the latest migration |
| `alembic current` | Show which migration the database is at |
| `alembic history` | List all migrations |
| `alembic revision --autogenerate -m "message"` | Create a new migration from changes in `app/models.py` |
| `alembic stamp head` | Mark a database as up to date without running anything (only for a database whose tables already exist) |

To change the database: edit `app/models.py`, run `alembic revision --autogenerate -m "describe the change"`, **read the generated file in `alembic/versions/`**, then run `alembic upgrade head`.

## Progress

- [x] Step 1: Project setup with FastAPI and basic endpoints
- [x] Step 2: CRUD endpoints for applications with Pydantic validation (in-memory)
- [x] Step 3: Store applications in PostgreSQL using SQLAlchemy
- [x] Step 4: Alembic migrations and the `job_link` column
- [ ] Step 5
- [ ] Step 6
- [ ] Step 7
- [ ] Step 8
- [ ] Step 9
