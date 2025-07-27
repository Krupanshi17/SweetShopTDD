from fastapi import HTTPException
from app.database import sweet_collection
from app.schemas.sweet_schema import SweetCreate, SweetUpdate
from bson import ObjectId

def obj_to_dict(sweet) -> dict:
    sweet["id"] = str(sweet["_id"])
    del sweet["_id"]
    return sweet

async def create_sweet(data: SweetCreate):
    sweet_dict = data.dict()
    result = await sweet_collection.insert_one(sweet_dict)
    sweet = await sweet_collection.find_one({"_id": result.inserted_id})
    return obj_to_dict(sweet)

async def get_all_sweets():
    sweets = []
    async for sweet in sweet_collection.find():
        sweets.append(obj_to_dict(sweet))
    return sweets

async def search_sweets(name: str = "", category: str = "", price_min: float = 0, price_max: float = 1e6):
    query = {
        "name": {"$regex": name, "$options": "i"},
        "category": {"$regex": category, "$options": "i"},
        "price": {"$gte": price_min, "$lte": price_max}
    }
    cursor = sweet_collection.find(query)
    return [obj_to_dict(s) async for s in cursor]

async def update_sweet(sweet_id: str, data: SweetUpdate):
    result = await sweet_collection.update_one({"_id": ObjectId(sweet_id)}, {"$set": data.dict(exclude_unset=True)})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    updated = await sweet_collection.find_one({"_id": ObjectId(sweet_id)})
    return obj_to_dict(updated)

async def delete_sweet(sweet_id: str):
    result = await sweet_collection.delete_one({"_id": ObjectId(sweet_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")

async def restock_sweet(sweet_id: str, quantity: int):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    sweet = await sweet_collection.find_one({"_id": ObjectId(sweet_id)})
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    new_quantity = sweet.get("quantity", 0) + quantity
    await sweet_collection.update_one(
        {"_id": ObjectId(sweet_id)},
        {"$set": {"quantity": new_quantity}}
    )

    updated = await sweet_collection.find_one({"_id": ObjectId(sweet_id)})
    return obj_to_dict(updated)