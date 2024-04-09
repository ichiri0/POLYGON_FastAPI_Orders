"""
API Проекта
"""

from fastapi import APIRouter

from .endpoints import orders, items, order_items

api_router = APIRouter()
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(order_items.router, prefix="/order_items", tags=["order_items"])
