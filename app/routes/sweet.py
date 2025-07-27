from fastapi import APIRouter, Depends, Header, HTTPException, Body
from typing import List
from jose import jwt, JWTError
from app.config import settings
from app.database import user_collection
from app.schemas.sweet_schema import SweetCreate, SweetUpdate, SweetResponse
from app.services import sweet_service

router = APIRouter(
    prefix="/api/sweets",
    tags=["Sweets"]
)

# Verify the admin user from the Authorization header token
async def verify_admin(authorization: str = Header(...)):
    # Check if Authorization header starts with 'Bearer '
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]

    # Decode JWT token and extract user ID
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token payload invalid")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch user from database
    user = await user_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # Verify user has admin role
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return user

# Public route to get all sweets
@router.get("/", response_model=List[SweetResponse])
async def get_all_sweets():
    return await sweet_service.get_all_sweets()

# Public route to search sweets by filters
@router.get("/search", response_model=List[SweetResponse])
async def search_sweets(name: str = "", category: str = "", price_min: float = 0, price_max: float = 1000):
    return await sweet_service.search_sweets(name, category, price_min, price_max)

# Admin route to create a new sweet
@router.post("/", status_code=201, response_model=SweetResponse)
async def create_sweet(
    admin=Depends(verify_admin),
    sweet: SweetCreate = Body(...)
):
    return await sweet_service.create_sweet(sweet)

# Admin route to update an existing sweet by ID
@router.put("/{sweet_id}", response_model=SweetResponse)
async def update_sweet(sweet_id: str, data: SweetUpdate, admin=Depends(verify_admin)):
    return await sweet_service.update_sweet(sweet_id, data)

# Admin route to delete a sweet by ID
@router.delete("/{sweet_id}")
async def delete_sweet(sweet_id: str, admin=Depends(verify_admin)):
    await sweet_service.delete_sweet(sweet_id)
    return {"message": "Sweet deleted"}

# Admin route to restock a sweet by ID, increasing its quantity
@router.patch("/{sweet_id}/restock", response_model=SweetResponse)
async def restock_sweet(sweet_id: str, quantity: int, admin=Depends(verify_admin)):
    return await sweet_service.restock_sweet(sweet_id, quantity)
