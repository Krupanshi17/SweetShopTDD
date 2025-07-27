# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr

# Schema for user registration
class UserCreate(BaseModel):
    email: EmailStr  # Validated email address
    password: str    # Plain password (will be hashed before storing)

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr  # Validated email address
    password: str    # Plain password for authentication

# Schema representing a user stored in the database
class UserInDB(BaseModel):
    id: str                # Unique user identifier (usually MongoDB ObjectId or UUID)
    email: EmailStr        # User's email
    hashed_password: str   # Hashed password stored in DB
    role: str = "user"     # Default role assigned to user (can be 'admin' or 'user')

# Schema for JWT token response after login or registration
class TokenResponse(BaseModel):
    access_token: str      # JWT token for authentication
    token_type: str = "bearer"  # Token type (usually 'bearer')
