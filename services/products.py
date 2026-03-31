from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas.products import ProductCreate
from repositories.products import ProductRepository
from models.product import Product

async def create_product(product: ProductCreate, db: AsyncSession, owner_id: int) -> Product:
    repo = ProductRepository(db)
    data = product.model_dump()
    data["owner_id"] = owner_id
    return await repo.create(data)

async def search_products(q: str, db: AsyncSession) -> List[Product]:
    repo = ProductRepository(db)
    return await repo.search(q)
