from fastapi import HTTPException
from app.database import user_collection
from app.utils.hash import hash_password, verify_password
from app.utils.auth import create_access_token
from app.schemas.user_schema import UserCreate, UserLogin

async def register_user(user: UserCreate):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    user_data = {"email": user.email, "hashed_password": hashed, "role": "user"}
    result = await user_collection.insert_one(user_data)

    token = create_access_token({"sub": str(result.inserted_id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

async def login_user(user: UserLogin):
    try:
        print("🔐 Login attempt:", user.email)
        
        db_user = await user_collection.find_one({"email": user.email})
        if not db_user:
            print("❌ No user found with this email")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print("🔍 DB User:", db_user)

        if not verify_password(user.password, db_user["hashed_password"]):
            print("❌ Password verification failed")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print("✅ Password matched. Creating token...")
        token = create_access_token({
            "sub": str(db_user["_id"]),
            "email": user.email
        })

        print("🎟️ Token:", token)
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print("🔥 Internal Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
# app/services/auth_service.py
from fastapi import HTTPException
from app.database import user_collection
from app.utils.hash import hash_password, verify_password
from app.utils.auth import create_access_token
from app.schemas.user_schema import UserCreate, UserLogin

async def register_user(user: UserCreate):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    user_data = {"email": user.email, "hashed_password": hashed, "role": "user"}
    result = await user_collection.insert_one(user_data)

    token = create_access_token({"sub": str(result.inserted_id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

async def login_user(user: UserLogin):
    try:
        print("🔐 Login attempt:", user.email)
        
        db_user = await user_collection.find_one({"email": user.email})
        if not db_user:
            print("❌ No user found with this email")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print("🔍 DB User:", db_user)

        if not verify_password(user.password, db_user["hashed_password"]):
            print("❌ Password verification failed")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print("✅ Password matched. Creating token...")
        token = create_access_token({
            "sub": str(db_user["_id"]),
            "email": user.email
        })

        print("🎟️ Token:", token)
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print("🔥 Internal Error:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")