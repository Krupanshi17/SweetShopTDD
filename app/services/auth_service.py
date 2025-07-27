# app/services/auth_service.py
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.database import user_collection
from app.config import settings
from app.schemas.user_schema import UserCreate, UserLogin
import uuid

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the plain password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token with optional expiration.
    If expires_delta is None, use default expiry from settings.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

async def register_user(user_data: UserCreate):
    """
    Register a new user.
    Raises HTTPException if email is already registered or
    if admin secret is invalid when role is admin.
    Returns access token on success.
    """
    # Check if user already exists
    existing_user = await user_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check admin secret if trying to register as admin
    if user_data.role == "admin":
        if not user_data.admin_secret or user_data.admin_secret != settings.ADMIN_SECRET:
            raise HTTPException(status_code=403, detail="Invalid admin secret")
    
    # Create user document with hashed password
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    user_doc = {
        "_id": user_id,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "role": user_data.role
    }
    
    # Insert user into DB
    await user_collection.insert_one(user_doc)
    
    # Generate access token for new user
    access_token = create_access_token(data={"sub": user_id})
    
    return {"access_token": access_token, "token_type": "bearer"}

async def login_user(user_data: UserLogin):
    """
    Authenticate user login.
    Raises HTTPException for invalid credentials.
    Returns access token on success.
    """
    try:
        user = await user_collection.find_one({"email": user_data.email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(user_data.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": str(user["_id"])})
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Login failed")


async def seed_admin():
    """
    Seed the default admin user if not exists.
    Uses admin email and password from settings.
    """
    existing_admin = await user_collection.find_one({"email": settings.ADMIN_EMAIL})
    if not existing_admin:
        admin_id = str(uuid.uuid4())
        hashed_password = hash_password(settings.ADMIN_PASSWORD)
        
        admin_doc = {
            "_id": admin_id,
            "email": settings.ADMIN_EMAIL,
            "hashed_password": hashed_password,
            "role": "admin"
        }
        
        await user_collection.insert_one(admin_doc)
        print(f"Admin user created with email: {settings.ADMIN_EMAIL}")
