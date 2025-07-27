# app/models/user_model.py
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    hashed_password: str
    role: str = "user"  # "user" or "admin"

    