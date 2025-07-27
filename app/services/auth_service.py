
from fastapi import HTTPException
from app.database import user_collection
from app.utils.hash import hash_password, verify_password
from app.utils.auth import create_access_token
from app.schemas.user_schema import UserCreate, UserLogin

async def register_user(user: UserCreate):
    # Check if the email already exists in the database
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the user password before saving
    hashed = hash_password(user.password)
    user_data = {"email": user.email, "hashed_password": hashed, "role": "user"}
    
    # Insert user data into MongoDB
    result = await user_collection.insert_one(user_data)

    # Generate JWT token for the new user
    token = create_access_token({"sub": str(result.inserted_id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}


async def login_user(user: UserLogin):
    try:
        # Find user by email in the database
        db_user = await user_collection.find_one({"email": user.email})
        if not db_user:
            # If user does not exist, raise invalid credentials error
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verify the provided password against the hashed password in DB
        if not verify_password(user.password, db_user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # If password matches, create JWT token for the user
        token = create_access_token({
            "sub": str(db_user["_id"]),
            "email": user.email
        })

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        # Log error (currently printed) and return 500 Internal Server Error
        print("Internal Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
