from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.items import ItemCreate
from repositories.items import ItemRepository
from models.item import Item

async def get_all_items(page: int, page_size: int, db: AsyncSession, in_stock: Optional[bool] = None) -> List[Item]:
    repo = ItemRepository(db)
    return await repo.get_all(page=page, page_size=page_size, in_stock=in_stock)

async def get_item(item_id: int, db: AsyncSession) -> Item:
    repo = ItemRepository(db)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

async def create_item(data: ItemCreate, db: AsyncSession) -> Item:
    repo = ItemRepository(db)
    return await repo.create(data.model_dump())

async def update_item(item_id: int, data: ItemCreate, db: AsyncSession) -> Item:
    repo = ItemRepository(db)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return await repo.update(item, data.model_dump())

async def delete_item(item_id: int, db: AsyncSession) -> None:
    repo = ItemRepository(db)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await repo.delete(item)
