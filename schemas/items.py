from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"

class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    category: Category
    in_stock: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category: Category
    in_stock: bool

    model_config = {"from_attributes": True}
