# JobTrack API

A REST API built with FastAPI to track job and internship applications.

## Tech Stack

- Python
- FastAPI
- Uvicorn (server)
- Git & GitHub

## Endpoints

| Method | Path      | Description                          |
|--------|-----------|--------------------------------------|
| GET    | `/`       | Confirms the API is running          |
| GET    | `/health` | Health check                         |
| GET    | `/about`  | Developer name, purpose, and skills  |

## How to Run (Windows)

```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --reload --port 8001
```

Then open:

- http://127.0.0.1:8001/
- http://127.0.0.1:8001/health
- http://127.0.0.1:8001/about
- http://127.0.0.1:8001/docs (interactive API docs)

## Progress

- [x] Step 1: Project setup with FastAPI and basic endpoints
- [ ] Step 2
- [ ] Step 3
- [ ] Step 4
- [ ] Step 5
- [ ] Step 6
- [ ] Step 7
- [ ] Step 8
- [ ] Step 9
