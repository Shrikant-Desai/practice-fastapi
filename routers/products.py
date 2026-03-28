from fastapi import APIRouter, status
from schemas.products import ProductCreate, ProductResponse
import services.products as products_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    return await products_service.create_product(product)
