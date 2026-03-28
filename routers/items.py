from fastapi import APIRouter, Query, Path, Depends
from typing import List, Optional
from core.dependencies import get_current_user, require_admin
from schemas.items import ItemCreate, ItemResponse
import services.items as items_service

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=List[ItemResponse])
async def get_all_items(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    in_stock: Optional[bool] = Query(None),
):
    return await items_service.get_all_items(page=page, page_size=page_size, in_stock=in_stock)

@router.get("/items/me")
async def get_item_msg():
    return {"msg": "this is your items profile"}

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int = Path(ge=0)):
    return await items_service.get_item(item_id)

@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(data: ItemCreate, current_user: dict = Depends(get_current_user)):
    return await items_service.create_item(data)

@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int, data: ItemCreate, current_user: dict = Depends(get_current_user)
):
    return await items_service.update_item(item_id, data)

@router.delete(
    "/{item_id}",
    status_code=204,
)
async def delete_item(item_id: int, current_user: dict = Depends(require_admin)):
    await items_service.delete_item(item_id)
