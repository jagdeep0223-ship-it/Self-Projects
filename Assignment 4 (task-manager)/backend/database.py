# Import the create_engine function from SQLAlchemy to establish a database connection.
from sqlalchemy import create_engine
# Import declarative_base from SQLAlchemy to define base class for models.
from sqlalchemy.ext.declarative import declarative_base
# Import sessionmaker from SQLAlchemy to create session factories.
from sqlalchemy.orm import sessionmaker

# Define the database URL using SQLite for local file-based storage.
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"

# Create the database engine with the URL and set check_same_thread to False for SQLite thread safety.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory bound to the engine, with autocommit and autoflush disabled.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for all database models using declarative_base.
Base = declarative_base()

# Define a generator function to provide database sessions.
def get_db():
    # Create a new database session.
    db = SessionLocal()
    # Use try-finally to ensure the session is closed after use.
    try:
        # Yield the session for use in dependencies.
        yield db
    finally:
        # Close the session to free resources.
        db.close()