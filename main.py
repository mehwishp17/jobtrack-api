# Import the FastAPI class - the main tool that builds our web API
from fastapi import FastAPI

# Create the app object. The title shows up in the auto-generated docs page (/docs)
app = FastAPI(title="JobTrack API")


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
