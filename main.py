from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import items, auth, protected, products
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Learning Backend", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(items.router, prefix="/v1")
app.include_router(auth.router, prefix="/v1")
app.include_router(protected.router, prefix="/v1")
app.include_router(products.router, prefix="/v1")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # Reshape Pydantic's error format into something cleaner for clients
    errors = {}
    for error in exc.errors():
        field = " → ".join(str(loc) for loc in error["loc"] if loc != "body")
        errors[field] = error["msg"].replace("Value error, ", "")

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "fields": errors,
        },
    )


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
