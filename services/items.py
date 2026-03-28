from fastapi import HTTPException
from typing import List, Optional
from schemas.items import ItemCreate
import repositories.items as items_repo

async def get_all_items(page: int, page_size: int, in_stock: Optional[bool] = None) -> List[dict]:
    return items_repo.get_all(page=page, page_size=page_size, in_stock=in_stock)

async def get_item(item_id: int) -> dict:
    item = items_repo.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

async def create_item(data: ItemCreate) -> dict:
    return items_repo.create(data)

async def update_item(item_id: int, data: ItemCreate) -> dict:
    item = items_repo.update(item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

async def delete_item(item_id: int) -> None:
    success = items_repo.delete(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
