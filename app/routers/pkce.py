from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from ..services.pkce import PKCEService
from ..schemas.pkce import PKCEItem, PKCEItemCreate

from ..utils.service_result import handle_result

from ..config.database import get_db

router = APIRouter(
    prefix="/pkce",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

def get_db_2():
    '''
    A get_db method explicitly for functions that aren't endpoints.
    '''
    SQLALCHEMY_DATABASE_URL = "sqlite:///./pkce.db"
    engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False},
    )

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Return the session
    return session

def non_endpoint_create_pkce(item: PKCEItemCreate): # type: ignore
    db = get_db_2()
    result = PKCEService(db).create_item(item)
    return handle_result(result)

def non_endpoint_find_state(state: str):
    db = get_db_2()
    result = PKCEService(db).get_item(state)
    return handle_result(result)

@router.post("/state/", response_model=PKCEItem)
async def create_item(item: PKCEItemCreate, db: get_db = Depends()): # type: ignore
    result = PKCEService(db).create_item(item)
    return handle_result(result)

@router.get("/state/{item_id}", response_model=PKCEItem)
async def get_item(item_id: str, db: get_db = Depends()): # type: ignore
    result = PKCEService(db).get_item(item_id)
    return handle_result(result)
