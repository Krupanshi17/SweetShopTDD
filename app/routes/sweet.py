from fastapi import APIRouter
from typing import List
from app.schemas.sweet_schema import SweetCreate, SweetUpdate, SweetResponse
from app.services import sweet_service

router = APIRouter(
    prefix="/api/sweets",
    tags=["Sweets"]
)

#  USER ACCESS
@router.get("/", response_model=List[SweetResponse])
async def get_all_sweets():
    return await sweet_service.get_all_sweets()

@router.get("/search", response_model=List[SweetResponse])
async def search_sweets(
    name: str = "", 
    category: str = "", 
    price_min: float = 0, 
    price_max: float = 1000,
):
    return await sweet_service.search_sweets(name, category, price_min, price_max)

#  ADMIN ONLY
@router.post("/", response_model=SweetResponse, status_code=201)
async def create_sweet(data: SweetCreate):
    return await sweet_service.create_sweet(data)

@router.put("/{sweet_id}", response_model=SweetResponse)
async def update_sweet(sweet_id: str, data: SweetUpdate):
    return await sweet_service.update_sweet(sweet_id, data)

@router.delete("/{sweet_id}")
async def delete_sweet(sweet_id: str):
    await sweet_service.delete_sweet(sweet_id)
    return {"message": "Sweet deleted"}

@router.patch("/{sweet_id}/restock", response_model=SweetResponse)
async def restock_sweet(sweet_id: str, quantity: int):
    return await sweet_service.restock_sweet(sweet_id, quantity)