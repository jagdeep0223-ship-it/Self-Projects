# Import necessary modules for FastAPI application setup.
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
# Import security schemes for OAuth2 password flow.
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# Import SQLAlchemy components for database modeling and sessions.
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
# Import datetime utilities for handling time-based operations.
from datetime import datetime, timedelta
# Import JWT library for token encoding and decoding.
import jwt  # PyJWT for token handling
# Import exception for invalid tokens.
from jwt.exceptions import InvalidTokenError
# Import os for environment variable access.
import os
# Import dotenv to load environment variables from .env file.
from dotenv import load_dotenv
# Import pandas for data manipulation.
import pandas as pd
# Import scikit-learn components for machine learning tasks.
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
# Import numpy for numerical operations.
import numpy as np
# Import for Pydantic models
from pydantic import BaseModel
# CORS
from fastapi.middleware.cors import CORSMiddleware
# Standard way for in-memory string CSV reading
from io import StringIO

# Load environment variables from .env file to access secrets like SECRET_KEY.
load_dotenv()  # Load .env for SECRET_KEY

# Set up the database URL for SQLite, using a local file for simplicity in demos.
SQLALCHEMY_DATABASE_URL = "sqlite:///./insightforge.db"
# Create the SQLAlchemy engine to connect to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Create a session maker for managing database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Define the base class for declarative models.
Base = declarative_base()

# Define a dependency function to get a database session, ensuring it's closed after use.
def get_db():
    db = SessionLocal()  # Create a new session.
    try:
        yield db  # Yield the session for use in dependencies.
    finally:
        db.close()  # Close the session after the request.

# Define the User model class inheriting from Base.
class User(Base):
    __tablename__ = "users"  # Set the table name.
    id = Column(Integer, primary_key=True, index=True)  # Primary key with indexing.
    email = Column(String, unique=True, index=True)  # Unique email with indexing.
    password = Column(String)  # Store hashed password (plaintext for demo).
    role = Column(String, default="viewer")  # Default role is viewer; can be admin.

# Define the Dataset model class.
class Dataset(Base):
    __tablename__ = "datasets"  # Set the table name.
    id = Column(Integer, primary_key=True, index=True)  # Primary key.
    filename = Column(String)  # Store the uploaded file name.
    uploaded_by = Column(Integer, ForeignKey("users.id"))  # Foreign key to user who uploaded.
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of upload.

# Define the Prediction model class.
class Prediction(Base):
    __tablename__ = "predictions"  # Set the table name.
    id = Column(Integer, primary_key=True, index=True)  # Primary key.
    dataset_id = Column(Integer, ForeignKey("datasets.id"))  # Foreign key to dataset.
    predicted_value = Column(Float)  # Store the ML predicted value.
    confidence = Column(Float)  # Store a confidence score (dummy for demo).
    insight_text = Column(String)  # Store the generated business insight text.

# Create all tables in the database if they don't exist.
Base.metadata.create_all(bind=engine)  # Create tables if not exist

# Initialize the FastAPI application instance.
app = FastAPI()

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define JWT configuration constants.
SECRET_KEY = os.getenv("SECRET_KEY")  # Get secret key from env.
ALGORITHM = "HS256"  # Algorithm for JWT encoding.
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time.

# Set up OAuth2 scheme for bearer token authentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to create a JWT access token with expiration.
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()  # Copy data to encode.
    if expires_delta:  # If expiration delta provided.
        expire = datetime.utcnow() + expires_delta  # Calculate expiration time.
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default to 15 minutes.
    to_encode.update({"exp": expire})  # Add expiration to payload.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the token.
    return encoded_jwt  # Return the token.

# Function to authenticate a user against the database.
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()  # Query for user by email.
    if not user or user.password != password:  # Check if user exists and password matches (plaintext for demo).
        return False  # Return false if invalid.
    return user  # Return user object if valid.

# Asynchronous function to get the current user from JWT token.
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(  # Define exception for invalid credentials.
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the token.
        email: str = payload.get("sub")  # Extract email from payload.
        if email is None:  # If no email in payload.
            raise credentials_exception  # Raise exception.
    except InvalidTokenError:  # Catch invalid token error.
        raise credentials_exception  # Raise exception.
    user = db.query(User).filter(User.email == email).first()  # Query for user.
    if user is None:  # If user not found.
        raise credentials_exception  # Raise exception.
    return user  # Return the user.

# Pydantic model for registration request body
class RegisterRequest(BaseModel):
    email: str          # Email is required
    password: str       # Password is required
    role: str = "viewer"  # Role is optional, defaults to viewer

# New model for login
class LoginRequest(BaseModel):
    username: str  # This matches OAuth2 spec (email in our case)
    password: str

# # Endpoint for user registration.
# @app.post("/register")
# def register(email: str, password: str, role: str = "viewer", db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter(User.email == email).first()  # Check if email exists.
#     if existing_user:  # If user already registered.
#         raise HTTPException(status_code=400, detail="Email already registered")  # Raise bad request.
#     user = User(email=email, password=password, role=role)  # Create new user object (hash password in prod).
#     db.add(user)  # Add to session.
#     db.commit()  # Commit to database.
#     db.refresh(user)  # Refresh object with DB values.
#     return {"msg": "User created"}  # Return success message.

# Updated register endpoint that reads from JSON body
@app.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user (password plaintext for demo only!)
    user = User(email=request.email, password=request.password, role=request.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"msg": "User created"}

# # Endpoint for user login.
# @app.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)  # Authenticate credentials.
#     if not user:  # If authentication fails.
#         raise HTTPException(  # Raise unauthorized exception.
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Set token expiration.
#     access_token = create_access_token(  # Create token with user data.
#         data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}  # Return token.

# Updated login endpoint accepting JSON
@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint for uploading dataset (CSV).
@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":  # Check if user is admin.
        raise HTTPException(status_code=403, detail="Admin access required")  # Raise forbidden if not.
    
    # Validate file extension.
    if not file.filename.endswith(".csv"):  # Check if file is CSV.
        raise HTTPException(status_code=400, detail="CSV only")  # Raise bad request if not.
    
    # Read file contents asynchronously.
    contents = await file.read()  # Read the uploaded file.
    df = pd.read_csv(StringIO(contents.decode('utf-8')))  # Parse as pandas DataFrame using modern StringIO.
    required_cols = ["date", "metric_value", "category"]  # Define required columns.
    if not all(col in df.columns for col in required_cols):  # Check if all required columns present.
        raise HTTPException(status_code=400, detail="Missing required columns")  # Raise if missing.
    
    # Create and save dataset metadata.
    dataset = Dataset(filename=file.filename, uploaded_by=current_user.id)  # Create dataset object.
    db.add(dataset)  # Add to session.
    db.commit()  # Commit.
    db.refresh(dataset)  # Refresh.
    
    # Process the data.
    processed_df = process_data(df)  # Call data processing function.
    predictions = run_ml_prediction(processed_df, dataset.id, db)  # Run ML and save predictions.
    
    return {"msg": "Upload successful", "dataset_id": dataset.id, "predictions": predictions}  # Return success.

# Function for data processing.
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    # Clean data by dropping nulls.
    df = df.dropna()  # Drop rows with null values.
    
    # Parse date column.
    df['date'] = pd.to_datetime(df['date'])  # Convert date to datetime.
    
    # Aggregate data.
    aggregated = df.groupby('date').agg({'metric_value': 'sum'}).reset_index()  # Group by date and sum metric.
    
    # Normalize data.
    aggregated['normalized_value'] = (aggregated['metric_value'] - aggregated['metric_value'].min()) / (aggregated['metric_value'].max() - aggregated['metric_value'].min())  # Min-max normalization.
    
    # Generate feature for ML.
    aggregated['day_num'] = (aggregated['date'] - aggregated['date'].min()).dt.days  # Add day number feature.
    return aggregated  # Return processed DataFrame.

# Function for running ML prediction.
def run_ml_prediction(df: pd.DataFrame, dataset_id: int, db: Session):
    # Prepare features and target.
    X = df[['day_num']]  # Features: day_num.
    y = df['metric_value']  # Target: metric_value.
    
    # Split data for training.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # 80/20 split.
    
    # Train the model.
    model = LinearRegression()  # Initialize Linear Regression model.
    model.fit(X_train, y_train)  # Fit the model.
    
    # Predict future value.
    next_day = df['day_num'].max() + 30  # Assume next month as +30 days.
    predicted_value = model.predict(np.array([[next_day]]))[0]  # Predict for next day.
    
    # Calculate dummy confidence.
    y_pred = model.predict(X_test)  # Predict on test set.
    mse = mean_squared_error(y_test, y_pred)  # Calculate MSE.
    confidence = 1 / (1 + mse)  # Simple confidence formula.
    
    # Generate business insight.
    last_value = df['metric_value'].iloc[-1]  # Get last actual value.
    change_pct = ((predicted_value - last_value) / last_value) * 100  # Calculate percentage change.
    if change_pct > 10:  # If significant increase.
        insight = f"🚀 Metric value is predicted to increase by {abs(change_pct):.2f}%. Growth opportunity ahead!"
    elif change_pct < -10:  # If significant decrease.
        insight = f"⚠️ Metric value is predicted to decrease by {abs(change_pct):.2f}%. Immediate intervention recommended."
    else:  # If stable.
        insight = f"📊 Metric value is predicted to change by {change_pct:.2f}%. Stable trend."
    
    # Save the prediction to DB.
    prediction = Prediction(dataset_id=dataset_id, predicted_value=predicted_value, confidence=confidence, insight_text=insight)  # Create prediction object.
    db.add(prediction)  # Add to session.
    db.commit()  # Commit.
    db.refresh(prediction)  # Refresh.
    
    return {"predicted_value": predicted_value, "confidence": confidence, "insight": insight}  # Return prediction data.

# Endpoint to get all datasets.
@app.get("/datasets")
def get_datasets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    datasets = db.query(Dataset).all()  # Query all datasets.
    return [{"id": d.id, "filename": d.filename, "created_at": d.created_at} for d in datasets]  # Return list of dicts.

# Endpoint to get insights for a dataset.
@app.get("/insights/{dataset_id}")
def get_insights(dataset_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    predictions = db.query(Prediction).filter(Prediction.dataset_id == dataset_id).all()  # Query predictions by dataset.
    if not predictions:  # If none found.
        raise HTTPException(status_code=404, detail="No predictions found")  # Raise not found.
    return [{"predicted_value": p.predicted_value, "confidence": p.confidence, "insight_text": p.insight_text} for p in predictions]  # Return list.