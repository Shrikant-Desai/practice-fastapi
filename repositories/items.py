from schemas.items import ItemCreate
from typing import List, Optional

items_db: dict[int, dict] = {}
current_id = 1

def get_all(page: int, page_size: int, in_stock: Optional[bool] = None) -> List[dict]:
    skip = (page - 1) * page_size
    items_list = list(items_db.values())

    if in_stock is not None:
        items_list = [x for x in items_list if x["in_stock"] == in_stock]

    return items_list[skip : skip + page_size]

def get_by_id(item_id: int) -> Optional[dict]:
    return items_db.get(item_id)

def create(data: ItemCreate) -> dict:
    global current_id
    item = {"id": current_id, **data.model_dump()}
    items_db[current_id] = item
    current_id += 1
    return item

def update(item_id: int, data: ItemCreate) -> Optional[dict]:
    if item_id in items_db:
        items_db[item_id].update(data.model_dump())
        return items_db[item_id]
    return None

def delete(item_id: int) -> bool:
    if item_id in items_db:
        del items_db[item_id]
        return True
    return False
