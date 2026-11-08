# date / datetime are the Python types for calendar dates and timestamps
from datetime import date, datetime
from typing import Optional

# Column types and helpers: Enum column, Date/DateTime columns, "now()" function in SQL
from sqlalchemy import Date, DateTime, Enum, Integer, String, Text, func
# Mapped / mapped_column is the modern SQLAlchemy way to declare columns with type hints
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base
# Reuse the same status list we already defined for the API
from .schemas import ApplicationStatus


# This class = the "applications" table. One object = one row
class Application(Base):
    # The real table name inside PostgreSQL
    __tablename__ = "applications"

    # Unique number for each row; the database auto-increments it for us
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Required text, max 100 chars (nullable=False means NOT NULL)
    company: Mapped[str] = mapped_column(String(100), nullable=False)
    # Required job title
    role: Mapped[str] = mapped_column(String(255), nullable=False)
    # Required location
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    # Optional whole number; Optional[int] makes the column nullable
    stipend: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # Status is stored as one of the four allowed values; default is Applied
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status"),
        nullable=False,
        default=ApplicationStatus.Applied,
    )
    # The date the application was sent
    applied_date: Mapped[date] = mapped_column(Date, nullable=False)
    # Optional long text (Text has no length limit)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # When the row was created; the DATABASE fills it with its current time
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
