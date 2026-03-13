from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field


class NewProduct(BaseModel):
    name: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    in_stock: bool = True


app = FastAPI(title="FastAPI Day 4 Assignment")

products: List[dict] = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]


def find_product(product_id: int) -> Optional[dict]:
    return next((p for p in products if p["id"] == product_id), None)


@app.get("/")
def health_check():
    return {"message": "FastAPI Day 4 assignment is running"}


@app.get("/products")
def list_products():
    return {"products": products, "total": len(products)}


@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(new_product: NewProduct):
    if any(p["name"].lower() == new_product.name.lower() for p in products):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product name already exists")

    next_id = max(p["id"] for p in products) + 1 if products else 1
    product = {"id": next_id, **new_product.dict()}
    products.append(product)
    return {"message": "Product added", "product": product}


@app.put("/products/discount")
def bulk_discount(
    category: str = Query(..., description="Category to discount"),
    discount_percent: int = Query(..., ge=1, le=99, description="Percent off"),
):
    updated: List[dict] = []
    for p in products:
        if p["category"] == category:
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated.append(p)

    if not updated:
        return {"message": f"No products found in category: {category}"}

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated),
        "updated_products": updated,
    }


@app.get("/products/audit")
def product_audit():
    in_stock_list = [p for p in products if p["in_stock"]]
    out_stock_list = [p for p in products if not p["in_stock"]]
    stock_value = sum(p["price"] * 10 for p in in_stock_list)
    priciest = max(products, key=lambda p: p["price"])
    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p["name"] for p in out_stock_list],
        "total_stock_value": stock_value,
        "most_expensive": {"name": priciest["name"], "price": priciest["price"]},
    }


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: Optional[int] = Query(None, gt=0, description="New price"),
    category: Optional[str] = Query(None, description="New category"),
    in_stock: Optional[bool] = Query(None, description="Set availability"),
):
    product = find_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if price is not None:
        product["price"] = price
    if category is not None:
        product["category"] = category
    if in_stock is not None:
        product["in_stock"] = in_stock

    return {"message": "Product updated", "product": product}


@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):
    product = find_product(product_id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)
    return {"message": f"Product '{product['name']}' deleted"}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = find_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
