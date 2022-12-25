from fastapi import APIRouter, Depends

from ..services.pkce import PKCEService
from ..schemas.pkce import PKCEItem, PKCEItemCreate

from ..utils.service_result import handle_result

from ..config.database import get_db

router = APIRouter(
    prefix="/pkce",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.post("/state/", response_model=PKCEItem)
async def create_item(item: PKCEItemCreate, db: get_db = Depends()): # type: ignore
    result = PKCEService(db).create_item(item)
    return handle_result(result)


@router.get("/state/{item_id}", response_model=PKCEItem)
async def get_item(item_id: str, db: get_db = Depends()): # type: ignore
    result = PKCEService(db).get_item(item_id)
    return handle_result(result)
