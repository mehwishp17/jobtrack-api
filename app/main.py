# Import the FastAPI class - the main tool that builds our web API
from fastapi import FastAPI

# Import the database engine and the Base class that knows about all our tables
from .database import Base, engine

# Importing models makes sure SQLAlchemy knows the "applications" table exists
from . import models  # noqa: F401

# Import the router that holds all the /applications endpoints
from .routers import applications

# Create any missing tables when the app starts (Alembic will replace this in Step 4).
# Tables that already exist are left alone, so your data is safe
Base.metadata.create_all(bind=engine)

# Create the app object. The title shows up in the auto-generated docs page (/docs)
app = FastAPI(title="JobTrack API")

# Plug the applications router into the app so its endpoints become available
app.include_router(applications.router)


# @app.get("/") means: when someone sends a GET request to "/", run the function below
@app.get("/")
def root():
    # Returning a Python dict - FastAPI automatically converts it to JSON
    return {"message": "JobTrack API is running"}


# Health check endpoint: lets us (or a server) quickly confirm the API is alive
@app.get("/health")
def health():
    # A tiny JSON reply that says everything is fine
    return {"status": "ok"}


# About endpoint: information about the developer and the project
@app.get("/about")
def about():
    return {
        # Developer name
        "name": "Mehwish Patel",
        # What this project is for
        "purpose": "A REST API to track job and internship applications",
        # A list of skills (a Python list becomes a JSON array)
        "skills": ["Python", "FastAPI", "REST APIs", "Git", "GitHub"],
    }
