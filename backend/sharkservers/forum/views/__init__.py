"""
sharkservers_api.

sharkservers-api

(C) 2023-present Adrian Ciołek (Qwizi)
"""
from fastapi import APIRouter

from .admin.categories import router as admin_categories_router
from .admin.posts import router as admin_posts_router
from .admin.threads import router as admin_threads_router
from .categories import router as categories_router
from .posts import router as posts_router
from .threads import router as threads_router

router_v1 = APIRouter(prefix="/v1/forum", tags=["forum"])
router_v1.include_router(categories_router, prefix="/categories")
router_v1.include_router(threads_router, prefix="/threads")
router_v1.include_router(
    posts_router,
    prefix="/posts",
)

admin_router_v1 = APIRouter(prefix="/v1/admin/forum", tags=["admin-forum"])
admin_router_v1.include_router(admin_categories_router, prefix="/categories")
admin_router_v1.include_router(admin_threads_router, prefix="/threads")
admin_router_v1.include_router(admin_posts_router, prefix="/posts")
