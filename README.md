# JobTrack API

A REST API built with FastAPI to track job and internship applications.

## Tech Stack

- Python
- FastAPI
- Uvicorn (server)
- PostgreSQL (database)
- SQLAlchemy (ORM) with psycopg 3 (driver)
- pydantic-settings (reads `.env`)
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

## Project Structure

```
.env.example           # Template for your private .env (never commit .env)
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

The `applications` table is created automatically when the app starts (Alembic migrations come in Step 4).

## How to Run (Windows)

```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload --reload-dir app --port 8001
```

Then open:

- http://127.0.0.1:8001/
- http://127.0.0.1:8001/health
- http://127.0.0.1:8001/about
- http://127.0.0.1:8001/docs (interactive API docs)

## Progress

- [x] Step 1: Project setup with FastAPI and basic endpoints
- [x] Step 2: CRUD endpoints for applications with Pydantic validation (in-memory)
- [x] Step 3: Store applications in PostgreSQL using SQLAlchemy
- [ ] Step 4
- [ ] Step 5
- [ ] Step 6
- [ ] Step 7
- [ ] Step 8
- [ ] Step 9
