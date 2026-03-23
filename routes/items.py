from fastapi import APIRouter, Query, HTTPException, Path
from pydantic import BaseModel, Field
from typing import List


router = APIRouter(prefix="/items", tags=["Items"])


items_db: dict[int, dict] = {}
current_id = 1


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    in_stock: bool = True


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool


@router.get("/", response_model=List[ItemResponse])
async def get_all_items(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=10, ge=1)
):
    skip = (page - 1) * page_size
    items = list(items_db.values())
    return items[skip : skip + page_size]


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int = Path(ge=0)):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(
    data: ItemCreate,
):
    global current_id
    item = {"id": current_id, **data.model_dump()}
    items_db[current_id] = item
    current_id += 1
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, data: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id].update(data.model_dump())
    return items_db[item_id]


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
