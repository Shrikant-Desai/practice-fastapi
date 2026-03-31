from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
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

    async def search(self, q: str) -> list[Product]:
        # Combine name and description into a tsvector for full-text search
        search_vector = func.to_tsvector(
            "english", Product.name + " " + func.coalesce(Product.description, "")
        )
        search_query = func.plainto_tsquery("english", q)

        stmt = select(Product).where(search_vector.op("@@")(search_query))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
