from sqlalchemy.ext.asyncio import AsyncSession
from schemas.products import ProductCreate
from repositories.products import ProductRepository
from models.product import Product

async def create_product(product: ProductCreate, db: AsyncSession, owner_id: int) -> Product:
    repo = ProductRepository(db)
    data = product.model_dump()
    data["owner_id"] = owner_id
    return await repo.create(data)
