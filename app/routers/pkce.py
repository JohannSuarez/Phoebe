from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from ..services.pkce import PKCEService
from ..schemas.pkce import PKCEItem, PKCEItemCreate
from ..utils.service_result import handle_result
from ..config.database import get_db
from dotenv import dotenv_values

import base64, requests

config = dotenv_values(".env")
router = APIRouter(
    prefix="/pkce",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

def get_db_2():
    """ 
    A get_db method explicitly for functions that aren't endpoints.
    """
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

'''
    Routes not in use.

@router.post("/state/", response_model=PKCEItem)
async def create_item(item: PKCEItemCreate, db: get_db = Depends()): # type: ignore
    result = PKCEService(db).create_item(item)
    return handle_result(result)

@router.get("/state/{item_id}", response_model=PKCEItem)
async def get_item(item_id: str, db: get_db = Depends()): # type: ignore
    result = PKCEService(db).get_item(item_id)
    return handle_result(result)
'''
@router.post("/renew_token")
async def renew_access_token(refresh_token: str):
    """
    An access token expires. A user provides a refresh token 
    to acquire a new pair of access and refresh tokens.

    For more information:
    https://dev.fitbit.com/build/reference/web-api/authorization/refresh-token/
    """

    client_id: str = config["CLIENT_ID"] or ""
    client_secret: str = config["CLIENT_SECRET"] or ""
    basic_token: str = client_id + ":" + client_secret
    basic_token = base64.b64encode(basic_token.encode('utf-8')).decode('utf-8')

    url = "https://api.fitbit.com/oauth2/token"
    headers = {
            "Authorization": f"Basic {basic_token}",
            "Content-Type": "application/x-www-form-urlencoded"}

    data = {"grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": refresh_token}

    response = requests.post(url, headers=headers, data=data).json()

    print(response)
    new_tokens = {"access_token": response['access_token'],
                  "refresh_token": response['refresh_token']
    }

    return new_tokens
