# app/db/crud/__init__.py
from .user_crud import router as user_router
from .tag_crud import router as tag_router
from .location_crud import router as location_router
from .attraction_crud import router as attraction_router
from .attraction_tag_crud import router as attraction_tag_router
from .attraction_review_crud import router as attraction_review_router

__all__ = [
    "user_router",
    "tag_router",
    "attraction_router",
    "attraction_tag_router",
    "attraction_review_router",
]