from pydantic import BaseModel, Field
from typing import Optional

# Model for creating a new sweet item
class SweetCreate(BaseModel):
    # Name of the sweet, required and must have at least 1 character
    name: str = Field(..., min_length=1)
    # Category of the sweet (e.g., Indian, Western)
    category: str
    # Price must be greater than 0
    price: float = Field(..., gt=0)
    # Quantity must be zero or more
    quantity: int = Field(..., ge=0)

# Model for updating an existing sweet item
class SweetUpdate(BaseModel):
    # All fields are optional for partial updates
    name: Optional[str]
    category: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

# Response model returned after creating, updating, or fetching a sweet
class SweetResponse(BaseModel):
    # Unique identifier for the sweet
    id: str
    name: str
    category: str
    price: float
    quantity: int
