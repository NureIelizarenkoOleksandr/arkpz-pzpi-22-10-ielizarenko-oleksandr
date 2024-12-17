from fastapi import APIRouter
from app.api.endpoints.goods import router as goods_router
from app.api.endpoints.sales import router as sales_router

router = APIRouter()

router.include_router(goods_router, prefix="/goods", tags=["Goods"])
router.include_router(sales_router, prefix="/sales", tags=["Sales"])