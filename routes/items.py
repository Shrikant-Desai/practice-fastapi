from fastapi import APIRouter, Query, HTTPException, Path, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from auth.dependencies import get_current_user, require_admin


router = APIRouter(prefix="/items", tags=["Items"])


items_db: dict[int, dict] = {}
current_id = 1


class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    category: Category
    in_stock: bool = True


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category: Category
    in_stock: bool


@router.get("/", response_model=List[ItemResponse])
async def get_all_items(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    in_stock: Optional[bool] = Query(None),
):
    skip = (page - 1) * page_size
    items_list = list(items_db.values())

    if in_stock is not None:
        items_list = [x for x in items_list if x["in_stock"] == in_stock]

    return items_list[skip : skip + page_size]


@router.get("/items/me")
async def get_item_msg():
    return {"msg": "this is your items profile"}


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int = Path(ge=0)):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(data: ItemCreate, current_user: dict = Depends(get_current_user)):
    global current_id
    item = {"id": current_id, **data.model_dump()}
    items_db[current_id] = item
    current_id += 1
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int, data: ItemCreate, current_user: dict = Depends(get_current_user)
):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id].update(data.model_dump())
    return items_db[item_id]


@router.delete(
    "/{item_id}",
    status_code=204,
)
async def delete_item(item_id: int, current_user: dict = Depends(require_admin)):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
