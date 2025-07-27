# app/utils/hash.py
from passlib.context import CryptContext

# Create a CryptContext object to handle password hashing using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash the plain password using bcrypt algorithm.
    
    Args:
        password (str): The plain text password to hash.
    
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the hashed password.
    
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The stored hashed password.
    
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
