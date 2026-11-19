"""Database plumbing: the engine (the connection) and the session factory."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Same .env as v1. The password is never written in code.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Check your .env file.")

# The scheme must be "postgresql+psycopg://". It tells SQLAlchemy to use
# Psycopg 3 as the driver (a bare "postgresql://" would look for psycopg2).

# The engine owns a pool of connections to Supabase. Create it once per app.
# pool_pre_ping tests a connection before using it, which avoids errors from
# connections the server closed while the app was idle.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# A session factory. Each call to SessionLocal() gives a new Session, which is
# a "workspace" that tracks the objects you load and the changes you make to them.
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """FastAPI dependency: give each request its own session, then always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
