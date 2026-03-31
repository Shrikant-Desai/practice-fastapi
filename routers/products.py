from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.products import ProductCreate, ProductResponse
import services.products as products_service
from core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("id")
    return await products_service.create_product(product, db, user_id)
