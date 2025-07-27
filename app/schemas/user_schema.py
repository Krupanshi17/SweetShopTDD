# app/schemas/user_schema.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    # Schema for user registration request
    email: EmailStr  # User's email address (validated)
    password: str    # User's password
    role: str = "user"  # User role, defaults to 'user'
    admin_secret: Optional[str] = None  # Optional secret key for admin registration

class UserLogin(BaseModel):
    # Schema for user login request
    email: EmailStr  # User's email address (validated)
    password: str    # User's password

class TokenResponse(BaseModel):
    # Schema for token response after successful login/registration
    access_token: str  # JWT access token string
    token_type: str = "bearer"  # Token type, defaults to 'bearer'
