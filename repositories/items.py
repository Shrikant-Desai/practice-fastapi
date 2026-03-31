from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.item import Item

class ItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, page: int, page_size: int, in_stock: bool | None = None) -> list[Item]:
        skip = (page - 1) * page_size
        stmt = select(Item)
        if in_stock is not None:
            stmt = stmt.where(Item.in_stock == in_stock)
        stmt = stmt.offset(skip).limit(page_size)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, item_id: int) -> Item | None:
        result = await self.db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Item:
        item = Item(**data)
        self.db.add(item)
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def update(self, item: Item, data: dict) -> Item:
        for key, value in data.items():
            setattr(item, key, value)
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        await self.db.delete(item)
        await self.db.flush()
