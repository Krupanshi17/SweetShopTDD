from pydantic import BaseModel, Field
from typing import Optional

class SweetCreate(BaseModel):
    name: str = Field(..., min_length=1)
    category: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

class SweetUpdate(BaseModel):
    name: Optional[str]
    category: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

class SweetResponse(BaseModel):
    id: str
    name: str
    category: str
    price: float
    quantity: int
