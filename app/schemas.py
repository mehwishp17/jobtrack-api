# date type is used for applied_date (a real calendar date like 2026-11-08)
from datetime import date
# Enum lets us define a fixed list of allowed values
from enum import Enum
# Optional means "this value may be missing (None)"
from typing import Optional

# BaseModel is the Pydantic class that gives us automatic data validation
# Field lets us add extra rules (like min length) to a single field
from pydantic import BaseModel, Field


# The only allowed statuses. Anything else (like "Maybe") is rejected with a 422 error
class ApplicationStatus(str, Enum):
    # Left side = Python name, right side = the text sent in JSON
    Applied = "Applied"
    Interview = "Interview"
    Offer = "Offer"
    Rejected = "Rejected"


# Shape of the data a client sends when CREATING an application
class ApplicationCreate(BaseModel):
    # Required text, must be between 1 and 100 characters
    company: str = Field(min_length=1, max_length=100)
    # Required text (the job title)
    role: str
    # Location of the job (required, as the spec lists it without "optional")
    location: str
    # Optional whole number; ge=0 means "greater than or equal to 0" (no negatives)
    stipend: Optional[int] = Field(default=None, ge=0)
    # Must be one of the ApplicationStatus values; defaults to Applied if not sent
    status: ApplicationStatus = ApplicationStatus.Applied
    # Date the application was sent, written as "YYYY-MM-DD"
    applied_date: date
    # Optional free-text notes
    notes: Optional[str] = None


# Shape of the data a client sends when UPDATING (PUT). Every field is optional,
# so the client can send only the fields they want to change
class ApplicationUpdate(BaseModel):
    # Same rules as before, but default=None means "not provided"
    company: Optional[str] = Field(default=None, min_length=1, max_length=100)
    role: Optional[str] = None
    location: Optional[str] = None
    stipend: Optional[int] = Field(default=None, ge=0)
    status: Optional[ApplicationStatus] = None
    applied_date: Optional[date] = None
    notes: Optional[str] = None


# Shape of the data we send BACK to the client: everything in Create, plus the id.
# Inheriting from ApplicationCreate avoids copy-pasting all the fields
class ApplicationOut(ApplicationCreate):
    # The unique number the server gave this application
    id: int
