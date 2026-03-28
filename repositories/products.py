from schemas.products import ProductCreate

fake_db = []

def create(product: ProductCreate) -> dict:
    new_product = product.model_dump()
    new_product["id"] = len(fake_db) + 1
    fake_db.append(new_product)
    return new_product
