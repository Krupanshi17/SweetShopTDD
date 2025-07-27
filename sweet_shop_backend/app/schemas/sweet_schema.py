from pydantic import BaseModel, Field
from typing import Optional

class SweetCreate(BaseModel):
    # Schema for creating a new sweet; all fields required
    name: str = Field(..., min_length=1)  # Name must be at least 1 character
    category: str  # Category of the sweet (e.g., Indian, Western)
    price: float = Field(..., gt=0)  # Price must be greater than 0
    quantity: int = Field(..., ge=0)  # Quantity must be zero or positive

class SweetUpdate(BaseModel):
    # Schema for updating an existing sweet; all fields optional
    name: Optional[str]
    category: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

class SweetResponse(BaseModel):
    # Schema for sweet data returned in API responses
    id: str = Field(..., alias="_id")  # Map MongoDB _id field to id in response
    name: str
    category: str
    price: float
    quantity: int

    class Config:
        allow_population_by_field_name = True  # Allow using "id" field name when returning responses
