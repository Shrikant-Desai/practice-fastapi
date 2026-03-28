from schemas.products import ProductCreate
import repositories.products as products_repo

async def create_product(product: ProductCreate) -> dict:
    return products_repo.create(product)
