# apps admin views
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def admin_index():
    return {"message": "Hello from apps module"}
