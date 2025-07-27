from pydantic import BaseModel, EmailStr

# Schema for user registration request payload
class RegisterRequest(BaseModel):
    full_name: str  # Full name of the user
    email: EmailStr  # Valid email address (validated by Pydantic)
    password: str  # User password (raw, will be hashed later)

# Schema for user login request payload
class LoginRequest(BaseModel):
    email: EmailStr  # Valid email address
    password: str  # User password
