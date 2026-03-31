import json

from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.items import ItemCreate
from repositories.items import ItemRepository
from models.item import Item
from cache.redis_client import get_cache, set_cache, delete_cache, delete_pattern


async def get_all_items(
    page: int, page_size: int, db: AsyncSession, in_stock: Optional[bool] = None
) -> List[Item]:
    repo = ItemRepository(db)

    # Cache list results too — but with a shorter TTL since they change more
    cache_key = f"products:list:{page}:{page_size}"
    cached = await get_cache(cache_key)
    if cached:
        return json.loads(cached)

    items = await repo.get_all(page=page, page_size=page_size, in_stock=in_stock)
    await set_cache(cache_key, json.dumps(items), ttl=300)  # 5 minutes
    return items


async def get_item(item_id: int, db: AsyncSession) -> Item:
    repo = ItemRepository(db)

    cache_key = f"item:{item_id}"

    # 1. Check cache first
    cached = await get_cache(cache_key)
    if cached:
        return json.loads(cached)  # cache hit — no DB query
    # 2. Cache miss — fetch from DB
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # 3. Store in cache for next time (TTL = 1 hour)
    await set_cache(cache_key, json.dumps(item), ttl=3600)
    return item


async def create_item(data: ItemCreate, db: AsyncSession) -> Item:
    repo = ItemRepository(db)
    item = await repo.create(data.model_dump())
    # Invalidate all list caches — new product affects every list
    await delete_pattern("products:list:*")
    return item


async def update_item(item_id: int, data: ItemCreate, db: AsyncSession) -> Item:
    repo = ItemRepository(db)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item = await repo.update(item, data.model_dump())
    # Invalidate the cache — stale data is worse than no cache
    await delete_cache(f"item:{item_id}")

    return item


async def delete_item(item_id: int, db: AsyncSession) -> None:
    repo = ItemRepository(db)
    item = await repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    await repo.delete(item)
