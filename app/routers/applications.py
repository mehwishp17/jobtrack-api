# APIRouter groups related endpoints; Depends injects helpers (like a DB session);
# HTTPException lets us return error codes like 404; status gives named HTTP codes
from fastapi import APIRouter, Depends, HTTPException, status

# List is used to describe "a list of ApplicationOut" in type hints
from typing import List

# Session is the type of a database session (used for type hints)
# select builds a SELECT query
from sqlalchemy import select
from sqlalchemy.orm import Session

# get_db gives each request its own database session
from ..database import get_db
# The table model (a row = an Application object)
from ..models import Application
# Our Pydantic models from schemas.py (".." means "one folder up", the app package)
from ..schemas import ApplicationCreate, ApplicationOut, ApplicationUpdate

# Every route here starts with /applications; tags groups them neatly in /docs
router = APIRouter(prefix="/applications", tags=["Applications"])


# Helper: find one application by id, or stop with a 404 error if it doesn't exist
def find_application(db: Session, application_id: int) -> Application:
    # db.get() looks up a row by its primary key; returns None if there is no such row
    item = db.get(Application, application_id)
    # Not found -> tell the client with a clear message
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with id {application_id} not found",
        )
    return item


# POST /applications -> create a new one. 201 means "Created"
@router.post("", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db)):
    # Turn the validated Pydantic data into a dict, then into a database object.
    # We do NOT set the id: PostgreSQL picks it automatically
    item = Application(**data.model_dump())
    # Stage the new row in the session
    db.add(item)
    # commit() really saves it to the database
    db.commit()
    # refresh() reloads the row so we get the id and created_at the database made
    db.refresh(item)
    # response_model converts the SQLAlchemy object to JSON (thanks to from_attributes)
    return item


# GET /applications -> return everything
@router.get("", response_model=List[ApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    # SELECT * FROM applications ORDER BY id; scalars().all() gives a list of objects
    return db.scalars(select(Application).order_by(Application.id)).all()


# GET /applications/{id} -> return one. {application_id} is taken from the URL
@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db)):
    # The helper raises a 404 automatically if it isn't found
    return find_application(db, application_id)


# PUT /applications/{id} -> change only the fields the client sent
@router.put("/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int, data: ApplicationUpdate, db: Session = Depends(get_db)
):
    # Get the existing row (404 if missing)
    item = find_application(db, application_id)
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
    # Copy each changed value onto the database object
    for field, value in changes.items():
        setattr(item, field, value)
    # Save the changes
    db.commit()
    # Reload the row so the response shows what is really stored
    db.refresh(item)
    return item


# DELETE /applications/{id} -> remove it. 204 means "success, nothing to send back"
@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    # Find it first (404 if missing)
    item = find_application(db, application_id)
    # Mark the row for deletion
    db.delete(item)
    # Make the deletion permanent
    db.commit()
    # Returning nothing matches the 204 "No Content" status
    return None
