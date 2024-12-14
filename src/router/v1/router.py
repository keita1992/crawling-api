from fastapi import APIRouter

from .endpoints import crawl

router = APIRouter()

router.include_router(crawl.router, tags=["v1"])
