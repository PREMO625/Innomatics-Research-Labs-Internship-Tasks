from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)


app = FastAPI(title="FastAPI Day 6 Assignment")

products: List[dict] = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

orders: List[dict] = []


def find_product(product_id: int) -> Optional[dict]:
    return next((p for p in products if p["id"] == product_id), None)


@app.get("/")
def health_check():
    return {"message": "FastAPI Day 6 assignment is running"}


@app.get("/products")
def list_products():
    return {"products": products, "total": len(products)}


@app.get("/products/search")
def search_products(keyword: str = Query(..., min_length=1)):
    results = [p for p in products if keyword.lower() in p["name"].lower()]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {"keyword": keyword, "total_found": len(results), "products": results}


@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price", description="Allowed: price, name"),
    order: str = Query("asc", description="Allowed: asc, desc"),
):
    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sort_by must be 'price' or 'name'")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="order must be 'asc' or 'desc'")

    sorted_products = sorted(products, key=lambda p: p[sort_by], reverse=(order == "desc"))
    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products,
        "total": len(sorted_products),
    }


@app.get("/products/page")
def paginate_products(
    page: int = Query(1, ge=1),
    limit: int = Query(2, ge=1, le=20),
):
    start = (page - 1) * limit
    total_pages = -(-len(products) // limit) if products else 0

    return {
        "page": page,
        "limit": limit,
        "total": len(products),
        "total_pages": total_pages,
        "products": products[start : start + limit],
    }


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def place_order(order: OrderRequest):
    product = find_product(order.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{product['name']} is out of stock")

    order_record = {
        "order_id": len(orders) + 1,
        "customer_name": order.customer_name,
        "product_id": order.product_id,
        "product": product["name"],
        "quantity": order.quantity,
        "unit_price": product["price"],
        "total_price": product["price"] * order.quantity,
        "status": "confirmed",
    }
    orders.append(order_record)
    return {"message": "Order placed", "order": order_record}


@app.get("/orders")
def list_orders():
    return {"orders": orders, "total_orders": len(orders)}


@app.get("/orders/search")
def search_orders(customer_name: str = Query(..., min_length=1)):
    results = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {"customer_name": customer_name, "total_found": len(results), "orders": results}


@app.get("/products/sort-by-category")
def sort_products_by_category():
    result = sorted(products, key=lambda p: (p["category"], p["price"]))
    return {"products": result, "total": len(result)}


@app.get("/products/browse")
def browse_products(
    keyword: Optional[str] = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20),
):
    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sort_by must be 'price' or 'name'")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="order must be 'asc' or 'desc'")

    result = products

    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))

    total_found = len(result)
    total_pages = -(-total_found // limit) if total_found else 0
    start = (page - 1) * limit
    paged_result = result[start : start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paged_result,
    }


@app.get("/orders/page")
def paginate_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20),
):
    start = (page - 1) * limit
    total_orders = len(orders)
    total_pages = -(-total_orders // limit) if total_orders else 0

    return {
        "page": page,
        "limit": limit,
        "total": total_orders,
        "total_pages": total_pages,
        "orders": orders[start : start + limit],
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = find_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
