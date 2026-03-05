from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Author: Geet Vilas Jamdal
# Notes: Clean, rewritten implementation for Assignment 1


class Product(BaseModel):
    id: int
    name: str
    price: int
    category: str
    in_stock: bool


app = FastAPI(title="E-commerce Store API - Assignment 1")


products: List[Product] = [
    Product(id=1, name="Wireless Mouse", price=299, category="Electronics", in_stock=True),
    Product(id=2, name="Notebook", price=49, category="Stationery", in_stock=True),
    Product(id=3, name="USB-C Cable", price=199, category="Electronics", in_stock=False),
    Product(id=4, name="Pen Set", price=99, category="Stationery", in_stock=True),
    Product(id=5, name="Laptop Stand", price=1299, category="Electronics", in_stock=True),
    Product(id=6, name="Mechanical Keyboard", price=2499, category="Electronics", in_stock=True),
    Product(id=7, name="Webcam", price=1899, category="Electronics", in_stock=False),
]


@app.get("/products")
def list_products():
    """Return all products and total count."""
    return {"products": [p.dict() for p in products], "total": len(products)}


@app.get("/products/category/{category_name}")
def products_by_category(category_name: str):
    """Return products for a given category."""
    matched = [p.dict() for p in products if p.category.lower() == category_name.lower()]
    if not matched:
        raise HTTPException(status_code=404, detail="No products found in this category")
    return {"category": category_name, "products": matched, "total": len(matched)}


@app.get("/products/instock")
def products_in_stock():
    """Return products that are currently in stock."""
    available = [p.dict() for p in products if p.in_stock]
    return {"in_stock_products": available, "count": len(available)}


@app.get("/store/summary")
def summary():
    """Return a short summary of the store (counts and categories)."""
    in_stock_count = sum(1 for p in products if p.in_stock)
    out_of_stock = len(products) - in_stock_count
    categories = sorted({p.category for p in products})
    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock,
        "categories": categories,
    }


@app.get("/products/search/{keyword}")
def search(keyword: str):
    """Case-insensitive name search."""
    matches = [p.dict() for p in products if keyword.lower() in p.name.lower()]
    if not matches:
        return {"message": "No products matched your search"}
    return {"keyword": keyword, "results": matches, "total_matches": len(matches)}


@app.get("/products/deals")
def deals():
    """Return the cheapest and most expensive product."""
    cheapest = min(products, key=lambda p: p.price)
    priciest = max(products, key=lambda p: p.price)
    return {"best_deal": cheapest.dict(), "premium_pick": priciest.dict()}


@app.get("/")
def health():
    return {"message": "FastAPI E-commerce Store API is running!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)