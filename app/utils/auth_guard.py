# app/utils/auth_guard.py
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from app.config import settings
from app.database import user_collection
from bson import ObjectId

async def get_current_user(authorization: str = Header(...)):
    """
    Extract and validate the JWT token from the Authorization header,
    decode it to retrieve the user ID, and fetch the corresponding user
    from the database.

    Raises HTTP 401 if token is missing/invalid or format is incorrect.
    Raises HTTP 404 if user not found in database.
    """
    # Check if header format is Bearer <token>
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        # Decode JWT token using secret key and algorithm
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Fetch user by ID from database
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        # Raise error if token is invalid or decoding fails
        raise HTTPException(status_code=401, detail="Invalid token")

async def require_admin(user=Depends(get_current_user)):
    """
    Dependency to enforce admin privileges.
    Raises HTTP 403 if the current user does not have admin role.
    """
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
