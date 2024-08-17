from fastapi import APIRouter, Depends
from auth.token_util import has_any_role, has_role

router = APIRouter(
    prefix="/api/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router.get("/admin", dependencies=[Depends(has_any_role(["USER", "ADMIN"]))])
async def get_private():
    return {"message": "Both Admin and user roles are permitted"}

@router.get("", dependencies=[Depends(has_role("USER"))])
async def get_private():
    return {"message": "Only user is allowed"}
