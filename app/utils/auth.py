# app/utils/auth.py
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode inside the token payload.

    Returns:
        str: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    # Set the token expiration time based on configured minutes
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add expiration claim to payload
    to_encode.update({"exp": expire})
    # Encode the token with the secret key and specified algorithm
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
