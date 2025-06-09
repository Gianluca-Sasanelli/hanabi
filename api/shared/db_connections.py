import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from collections.abc import Generator
from sqlalchemy.orm import Session

load_dotenv()

SUPABASE_CONNECTION_SESSION_POOLING = os.getenv("SUPABASE_CONNECTION_SESSION_POOLING")
engine = create_engine(
    SUPABASE_CONNECTION_SESSION_POOLING,
    pool_size=5,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_postgres_session() -> Generator[Session, None, None]:
    """Get SQLAlchemy session for PostgreSQL."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_postgres_url() -> str:
    """Get PostgreSQL connection URL."""
    return SUPABASE_CONNECTION_SESSION_POOLING
