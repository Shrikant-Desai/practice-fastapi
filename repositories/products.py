from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Product:
        product = Product(**data)
        self.db.add(product)
        await self.db.flush()
        await self.db.refresh(product)
        return product
