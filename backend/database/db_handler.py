# backend/database/db_handler.py
import os
import logging
from contextlib import contextmanager
from typing import Generator, Any, List, Optional, Dict

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session

from backend.config import settings
from backend.database.models import Base

# Set up logging
logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    """Initialize the database, creating tables if they don't exist."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

@contextmanager
def get_db() -> Generator:
    """
    Get a database session.
    
    Usage:
    ```
    with get_db() as db:
        user = db.query(User).filter(User.id == 1).first()
    ```
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()

# Generic CRUD operations
def create(db: Session, model, obj_in: Dict[str, Any]) -> Any:
    """Create a new database record."""
    db_obj = model(**obj_in)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get(db: Session, model, id: Any) -> Any:
    """Get a record by ID."""
    return db.query(model).filter(model.id == id).first()

def get_by_field(db: Session, model, field_name: str, value: Any) -> Any:
    """Get a record by a specific field value."""
    field = getattr(model, field_name)
    return db.query(model).filter(field == value).first()

def get_multi(db: Session, model, skip: int = 0, limit: int = 100) -> List:
    """Get multiple records with pagination."""
    return db.query(model).offset(skip).limit(limit).all()

def update(db: Session, db_obj, obj_in: Dict[str, Any]) -> Any:
    """Update a database record."""
    # Update model attributes
    for key, value in obj_in.items():
        if hasattr(db_obj, key):
            setattr(db_obj, key, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, db_obj) -> Any:
    """Delete a database record."""
    db.delete(db_obj)
    db.commit()
    return db_obj

def get_table_names() -> List[str]:
    """Get all table names in the database."""
    inspector = inspect(engine)
    return inspector.get_table_names()

# Command-line interface for database initialization
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database management tool")
    parser.add_argument("--init", action="store_true", help="Initialize the database")
    parser.add_argument("--tables", action="store_true", help="List all tables")
    args = parser.parse_args()
    
    if args.init:
        init_db()
        print("Database initialized successfully")
    
    if args.tables:
        tables = get_table_names()
        print(f"Database tables ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")