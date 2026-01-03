# Import BaseModel from Pydantic for defining data models.
from pydantic import BaseModel
# Import Optional from typing for optional fields.
from typing import Optional
# Import datetime for handling date-time fields.
from datetime import datetime

# Define UserBase model with username field.
class UserBase(BaseModel):
    # Specify the username as a string.
    username: str

# Define UserCreate model inheriting from UserBase (no additional fields).
class UserCreate(UserBase):
    # Pass to indicate no new fields.
    pass

# Define User model inheriting from UserBase.
class User(UserBase):
    # Add id field as integer.
    id: int

    # Inner Config class for model settings.
    class Config:
        # Enable ORM mode for compatibility with SQLAlchemy.
        from_attributes = True  # Enables ORM mode for SQLAlchemy

# Define TaskBase model with title field.
class TaskBase(BaseModel):
    # Specify the title as a string.
    title: str

# Define TaskCreate model inheriting from TaskBase (no additional fields).
class TaskCreate(TaskBase):
    # Pass to indicate no new fields.
    pass

# Define Task model inheriting from TaskBase.
class Task(TaskBase):
    # Add id field as integer.
    id: int
    # Add kept_by_user_id as optional integer.
    kept_by_user_id: Optional[int] = None
    # Add start_time as optional datetime.
    start_time: Optional[datetime] = None
    # Add stop_time as optional datetime.
    stop_time: Optional[datetime] = None

    # Inner Config class for model settings.
    class Config:
        # Enable ORM mode for compatibility with SQLAlchemy.
        from_attributes = True  # Enables ORM mode

# Define ActionRequest model for action payloads.
class ActionRequest(BaseModel):
    # Specify the username as a string.
    username: str  # Username sent in body for actions