from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from enum import Enum
import bleach

class ProductCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0, le=999999.99)
    category: ProductCategory
    sku: str = Field(..., pattern=r"^[A-Z]{2}-\d{4}$")
    description: Optional[str] = Field(default=None, max_length=1000)
    discount_price: Optional[float] = None

    @field_validator("name", mode="before")
    @classmethod
    def clean_name(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @field_validator("description")
    @classmethod
    def clean_description(cls, v):
        if v is None:
            return v
        v = v.strip()
        return bleach.clean(v, tags=["b", "i", "em", "strong"], strip=True)

    @model_validator(mode="after")
    def check_discount(self):
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("Discounted price must be less than price")
        return self

class ProductResponse(ProductCreate):
    id: int
