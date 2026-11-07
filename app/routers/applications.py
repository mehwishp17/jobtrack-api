# APIRouter groups related endpoints; HTTPException lets us return error codes like 404;
# Response/status give us named HTTP status codes
from fastapi import APIRouter, HTTPException, status

# List is used to describe "a list of ApplicationOut" in type hints
from typing import List

# Import our data models from schemas.py (".." means "one folder up", i.e. the app package)
from ..schemas import ApplicationCreate, ApplicationOut, ApplicationUpdate

# Every route here starts with /applications; tags groups them neatly in /docs
router = APIRouter(prefix="/applications", tags=["Applications"])

# Our fake "database": a plain Python list that lives in memory.
# WARNING: it resets every time the server restarts (we add a real database later)
applications: List[dict] = []

# Counter for ids. Each new application gets the next number (1, 2, 3, ...)
next_id = 1


# Helper: find one application by id, or stop with a 404 error if it doesn't exist
def find_application(application_id: int) -> dict:
    # Look through every stored application
    for item in applications:
        # If the id matches, we found it
        if item["id"] == application_id:
            return item
    # Loop finished without a match, so tell the client it was not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Application with id {application_id} not found",
    )


# POST /applications -> create a new one. 201 means "Created"
@router.post("", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def create_application(data: ApplicationCreate):
    # "global" lets us change the next_id variable defined outside this function
    global next_id
    # model_dump() turns the validated Pydantic object into a normal dict
    item = data.model_dump()
    # Add the id the server picked
    item["id"] = next_id
    # Move the counter forward so the next one gets a new id
    next_id += 1
    # Save it in our in-memory list
    applications.append(item)
    # response_model makes FastAPI return it in the ApplicationOut shape
    return item


# GET /applications -> return everything
@router.get("", response_model=List[ApplicationOut])
def list_applications():
    return applications


# GET /applications/{id} -> return one. {application_id} is taken from the URL
@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int):
    # The helper raises a 404 automatically if it isn't found
    return find_application(application_id)


# PUT /applications/{id} -> change only the fields the client sent
@router.put("/{application_id}", response_model=ApplicationOut)
def update_application(application_id: int, data: ApplicationUpdate):
    # Get the existing item (404 if missing)
    item = find_application(application_id)
    # exclude_unset=True keeps ONLY fields the client actually sent,
    # so fields they left out stay unchanged
    changes = data.model_dump(exclude_unset=True)
    # Required fields must not be set to null (e.g. {"company": null})
    for field in ("company", "role", "location", "status", "applied_date"):
        if field in changes and changes[field] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"{field} cannot be null",
            )
    # Apply the changes onto the stored item
    item.update(changes)
    return item


# DELETE /applications/{id} -> remove it. 204 means "success, nothing to send back"
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int):
    # Find it first (404 if missing)
    item = find_application(application_id)
    # Remove it from the list
    applications.remove(item)
    # Returning nothing matches the 204 "No Content" status
    return None
