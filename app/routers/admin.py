from fastapi import APIRouter, Depends
from auth.tokan_util import has_role

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.get("", dependencies=[Depends(has_role("admin"))])
async def get_private():
    return {"message": "Only admin role permitted"}

@router.get("/details", dependencies=[Depends(has_role("ADMIN"))])
async def get_private():
    return {"message": "Only admin role is allowed for details"}
