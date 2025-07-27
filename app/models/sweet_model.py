# app/models/sweet_model.py
from pydantic import BaseModel

class Sweet(BaseModel):
    # Name of the sweet item
    name: str
    
    # Category/type of the sweet (e.g., Indian, Western)
    category: str
    
    # Price of the sweet in the chosen currency
    price: float
    
    # Available quantity of the sweet item in stock
    quantity: int
