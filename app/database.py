# create_engine builds the connection to the database
# sessionmaker makes a factory that creates database sessions
# DeclarativeBase is the parent class for all our table models
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Our settings object (holds DATABASE_URL from .env)
from .config import settings

# The engine manages the actual connections to PostgreSQL.
# pool_pre_ping=True checks a connection is still alive before using it
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# SessionLocal() creates a new session = one "conversation" with the database.
# autoflush=False and autocommit=False mean we decide exactly when to save (commit)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Every model (table) we write will inherit from this Base class,
# so SQLAlchemy can keep track of all our tables
class Base(DeclarativeBase):
    pass


# A "dependency": FastAPI calls this for each request that asks for it via Depends(get_db)
def get_db():
    # Open a new session for this request
    db = SessionLocal()
    try:
        # "yield" hands the session to the endpoint and pauses here
        yield db
    finally:
        # After the endpoint finishes (even if it crashed), always close the session
        db.close()
