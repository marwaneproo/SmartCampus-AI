from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator

# Database configurations
# Adjust the database URL according to your PostgreSQL setup
DATABASE_URL = "postgresql://postgres.wwrqrcotszuuldoqnqxh:Emsi1Emsi2Emsi3@aws-1-eu-west-2.pooler.supabase.com:5432/postgres"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using them
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency function to get database session.
    Used for dependency injection in FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


