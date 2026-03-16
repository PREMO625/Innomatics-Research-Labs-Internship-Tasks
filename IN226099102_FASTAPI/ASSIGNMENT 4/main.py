from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=1)
    delivery_address: str = Field(..., min_length=1)


app = FastAPI(title="FastAPI Day 5 Assignment")

products: List[dict] = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

cart: List[dict] = []
orders: List[dict] = []


def find_product(product_id: int) -> Optional[dict]:
    return next((p for p in products if p["id"] == product_id), None)


def calculate_total(product: dict, quantity: int) -> int:
    return product["price"] * quantity


@app.get("/")
def health_check():
    return {"message": "FastAPI Day 5 assignment is running"}


@app.get("/products")
def list_products():
    return {"products": products, "total": len(products)}


@app.post("/cart/add")
def add_to_cart(
    product_id: int = Query(..., ge=1, description="ID of the product to add"),
    quantity: int = Query(1, ge=1, description="Quantity to add"),
):
    product = find_product(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{product['name']} is out of stock")

    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = calculate_total(product, item["quantity"])
            return {"message": "Cart updated", "cart_item": item}

    new_item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": calculate_total(product, quantity),
    }
    cart.append(new_item)
    return {"message": "Added to cart", "cart_item": new_item}


@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty", "items": [], "item_count": 0, "grand_total": 0}

    grand_total = sum(item["subtotal"] for item in cart)
    return {"items": cart, "item_count": len(cart), "grand_total": grand_total}


@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):
    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": f"Removed {item['product_name']} from cart"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart")


@app.post("/cart/checkout")
def checkout(request: CheckoutRequest):
    if not cart:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty — add items first")

    placed_orders: List[dict] = []
    for item in cart:
        order = {
            "order_id": len(orders) + len(placed_orders) + 1,
            "customer_name": request.customer_name,
            "delivery_address": request.delivery_address,
            "product_id": item["product_id"],
            "product": item["product_name"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price"],
            "total_price": item["subtotal"],
        }
        placed_orders.append(order)

    orders.extend(placed_orders)
    grand_total = sum(o["total_price"] for o in placed_orders)
    cart.clear()
    return {"message": "Checkout successful", "orders_placed": placed_orders, "grand_total": grand_total}


@app.get("/orders")
def list_orders():
    return {"orders": orders, "total_orders": len(orders)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
