from fastapi import APIRouter, Depends
from auth.token_util import valid_access_token

router = APIRouter(
    prefix="/api",
    tags=["general"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
def public():
    return {"message": "alive"}

@router.get("/public")
async def get_public():
    return {"message": "This endpoint is public"}

@router.get("/private", dependencies=[Depends(valid_access_token)])
async def get_private():
    return {"message": "This endpoint is private, for any one that is loffed in"}
