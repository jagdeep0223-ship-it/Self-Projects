    # Import FastAPI for creating the API application.
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
# Import Session from SQLAlchemy ORM for database sessions.
from sqlalchemy.orm import Session
# Import IntegrityError from SQLAlchemy for handling unique constraint errors.
from sqlalchemy.exc import IntegrityError
# Import models module for database models.
import models
# Import schemas module for Pydantic models.
import schemas
# Import engine and get_db from database module.
from database import engine, get_db
# Import datetime for handling current time.
from datetime import datetime, timezone

# Create all database tables using the Base metadata and engine.
models.Base.metadata.create_all(bind=engine)

# Instantiate the FastAPI application.
app = FastAPI()

# Add CORS middleware to allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define a startup event handler to populate initial data.
@app.on_event("startup")
def startup_event():
    # Get a database session using the dependency.
    db = next(get_db())
    # Check if there are no tasks in the database.
    if db.query(models.Task).count() == 0:
        # Create a list of sample Task objects.
        sample_tasks = [
            models.Task(title="Task 1"),
            models.Task(title="Task 2"),
            models.Task(title="Task 3"),
            models.Task(title="Task 4"),
            models.Task(title="Task 5"),
        ]
        # Add all sample tasks to the session.
        db.add_all(sample_tasks)
        # Commit the changes to the database.
        db.commit()
    # Check if a test user exists.
    if db.query(models.User).filter(models.User.username == "testuser").first() is None:
        # Create a test User object.
        test_user = models.User(username="testuser")
        # Add the test user to the session.
        db.add(test_user)
        # Commit the changes to the database.
        db.commit()

# Define a helper function to get or create a user by username.
def get_or_create_user(db: Session, username: str):
    # Query for the user by username.
    user = db.query(models.User).filter(models.User.username == username).first()
    # If user does not exist, create one.
    if not user:
        # Instantiate a new User object.
        user = models.User(username=username)
        # Use try-except to handle potential integrity errors.
        try:
            # Add the user to the session.
            db.add(user)
            # Commit the changes.
            db.commit()
            # Refresh the user object with database values.
            db.refresh(user)
        # Catch IntegrityError if username already exists (race condition).
        except IntegrityError:
            # Rollback the transaction.
            db.rollback()
            # Re-query for the user.
            user = db.query(models.User).filter(models.User.username == username).first()
    # Return the user object.
    return user

# Define GET endpoint for fetching the task queue.
@app.get("/queue", response_model=list[schemas.Task])
def get_queue(db: Session = Depends(get_db)):
    # Query all tasks where kept_by_user_id is None and return them.
    return db.query(models.Task).filter(models.Task.kept_by_user_id == None).all()

# Define GET endpoint for fetching user's tasks.
@app.get("/my_tasks", response_model=list[schemas.Task])
def get_my_tasks(username: str, db: Session = Depends(get_db)):
    # Get or create the user.
    user = get_or_create_user(db, username)
    # Query tasks kept by the user and return them.
    return db.query(models.Task).filter(models.Task.kept_by_user_id == user.id).all()

# Define POST endpoint for keeping a task (assign without starting).
@app.post("/keep/{task_id}")
def keep_task(task_id: int, request: schemas.ActionRequest, db: Session = Depends(get_db)):
    # Query the task by id.
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    # If task not found, raise 404 exception.
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # If task already taken, raise 400 exception.
    if task.kept_by_user_id is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task already taken")
    # Get or create the user.
    user = get_or_create_user(db, request.username)
    # Assign the task to the user.
    task.kept_by_user_id = user.id
    # Commit the changes.
    db.commit()
    # Return success message.
    return {"message": "Task kept"}

# Define POST endpoint for assigning a task (assign and start).
@app.post("/assign/{task_id}")
def assign_task(task_id: int, request: schemas.ActionRequest, db: Session = Depends(get_db)):
    # Query the task by id.
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    # If task not found, raise 404 exception.
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # If task already taken, raise 400 exception.
    if task.kept_by_user_id is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task already taken")
    # Get or create the user.
    user = get_or_create_user(db, request.username)
    # Assign the task to the user.
    task.kept_by_user_id = user.id
    # Set the start time to current UTC time.
    task.start_time = datetime.now(timezone.utc)  # Set start time automatically
    # Commit the changes.
    db.commit()
    # Return success message.
    return {"message": "Task assigned and started"}

# Define POST endpoint for starting a task.
@app.post("/start/{task_id}")
def start_task(task_id: int, request: schemas.ActionRequest, db: Session = Depends(get_db)):
    # Query the task by id.
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    # If task not found, raise 404 exception.
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # Get or create the user.
    user = get_or_create_user(db, request.username)
    # If not the user's task, raise 403 exception.
    if task.kept_by_user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your task")
    # If already started, raise 400 exception.
    if task.start_time is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task already started")
    # Set the start time to current UTC time.
    task.start_time = datetime.now(timezone.utc)
    # Commit the changes.
    db.commit()
    # Return success message.
    return {"message": "Task started"}

# Define POST endpoint for stopping a task.
@app.post("/stop/{task_id}")
def stop_task(task_id: int, request: schemas.ActionRequest, db: Session = Depends(get_db)):
    # Query the task by id.
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    # If task not found, raise 404 exception.
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # Get or create the user.
    user = get_or_create_user(db, request.username)
    # If not the user's task, raise 403 exception.
    if task.kept_by_user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your task")
    # If not started, raise 400 exception.
    if task.start_time is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task not started")
    # If already stopped, raise 400 exception.
    if task.stop_time is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task already stopped")
    # Set the stop time to current UTC time.
    task.stop_time = datetime.now(timezone.utc)
    # Commit the changes.
    db.commit()
    # Return success message.
    return {"message": "Task stopped"}