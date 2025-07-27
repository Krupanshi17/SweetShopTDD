from fastapi import HTTPException
from app.database import sweet_collection
from app.schemas.sweet_schema import SweetCreate, SweetUpdate
from bson import ObjectId

# Convert MongoDB object (_id) to dictionary with string id
def obj_to_dict(sweet) -> dict:
    sweet["id"] = str(sweet["_id"])
    del sweet["_id"]
    return sweet

# Create a new sweet in the database
async def create_sweet(data: SweetCreate):
    sweet_dict = data.dict()
    result = await sweet_collection.insert_one(sweet_dict)  # Insert sweet into MongoDB
    sweet = await sweet_collection.find_one({"_id": result.inserted_id})  # Fetch inserted sweet
    return obj_to_dict(sweet)

# Fetch all sweets from the database
async def get_all_sweets():
    sweets = []
    async for sweet in sweet_collection.find():
        sweets.append(obj_to_dict(sweet))
    return sweets

# Search sweets by name, category, and price range
async def search_sweets(name: str = "", category: str = "", price_min: float = 0, price_max: float = 1e6):
    query = {
        "name": {"$regex": name, "$options": "i"},  # Case-insensitive search
        "category": {"$regex": category, "$options": "i"},
        "price": {"$gte": price_min, "$lte": price_max}
    }
    cursor = sweet_collection.find(query)
    return [obj_to_dict(s) async for s in cursor]

# Update an existing sweet by its ID
async def update_sweet(sweet_id: str, data: SweetUpdate):
    result = await sweet_collection.update_one({"_id": ObjectId(sweet_id)}, {"$set": data.dict(exclude_unset=True)})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")
    updated = await sweet_collection.find_one({"_id": ObjectId(sweet_id)})
    return obj_to_dict(updated)

# Delete a sweet by its ID
async def delete_sweet(sweet_id: str):
    result = await sweet_collection.delete_one({"_id": ObjectId(sweet_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sweet not found")

# Restock an existing sweet by adding quantity
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
