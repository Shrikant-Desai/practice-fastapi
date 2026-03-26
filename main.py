from fastapi import APIRouter, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from routes import items, auth, protected

app = FastAPI(title="Learning Backend", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(items.router, prefix="/v1")
app.include_router(auth.router)
app.include_router(protected.router)


# v1 = APIRouter(prefix="/v1")


# @v1.get("/items")
# async def get_items(response: Response):

#     response.headers["Cache-Control"] = "public, max-age=60"  # 1 minute
#     response.headers["ETag"] = f'"items-v1"'  # fingerprint of content

#     return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]


# @v1.post("/items")
# async def create_item(response: Response):

#     response.headers["Cache-Control"] = "no-store"  # prevent caching

#     return {"id": 3, "name": "Item 3"}


# @v1.delete("/items/{item_id}")
# async def delete_item(item_id: int, response: Response):

#     response.headers["Cache-Control"] = "no-store"  # prevent caching

#     return {"message": f"Item {item_id} deleted"}


# app.include_router(v1)
