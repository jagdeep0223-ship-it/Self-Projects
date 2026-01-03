# Import necessary column types and functions from SQLAlchemy.
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# Import relationship from SQLAlchemy ORM for defining associations.
from sqlalchemy.orm import relationship
# Import the Base class from the database module.
from database import Base
# Import datetime and timezone
from datetime import datetime, timezone

# Define the User model class inheriting from Base.
class User(Base):
    # Set the table name for the User model.
    __tablename__ = "users"

    # Define the id column as primary key with indexing.
    id = Column(Integer, primary_key=True, index=True)
    # Define the username column as unique string with indexing.
    username = Column(String, unique=True, index=True)  # Unique username for each user

    # Define a relationship to Task model, back-populating the user field.
    tasks = relationship("Task", back_populates="user")  # Relationship to tasks kept by this user

# Define the Task model class inheriting from Base.
class Task(Base):
    # Set the table name for the Task model.
    __tablename__ = "tasks"

    # Define the id column as primary key with indexing.
    id = Column(Integer, primary_key=True, index=True)
    # Define the title column as string with indexing.
    title = Column(String, index=True)  # Task title, e.g., "Task 1"
    # Define the kept_by_user_id column as foreign key to users.id, nullable.
    kept_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null if in queue
    # Define the start_time column as DateTime with timezone=True, nullable.
    start_time = Column(DateTime(timezone=True), nullable=True)  # Start time, if started (aware)
    # Define the stop_time column as DateTime with timezone=True, nullable.
    stop_time = Column(DateTime(timezone=True), nullable=True)  # Stop time, if stopped (aware)

    # Define a relationship to User model, back-populating the tasks field.
    user = relationship("User", back_populates="tasks")  # Relationship to the user who kept it