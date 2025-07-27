# app/models/user_model.py
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr  # User's email, validated as proper email format
    hashed_password: str  # Hashed password stored securely
    role: str = "user"  # User role, default is "user"; can also be "admin"
