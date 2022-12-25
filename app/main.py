from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas.pkce import PKCEItemCreate
from .utils.app_exceptions import AppExceptionCase
from .routers import auth_url, pkce
from .config.database import create_tables
from dotenv import dotenv_values

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .utils.request_exceptions import (
        http_exception_handler,
        request_validation_exception_handler
)

from .utils.app_exceptions import app_exception_handler

import base64


create_tables()

config = dotenv_values(".env")
# These variables have to be checked otherwise, we raise an Exception
# because the app is useless without these.
# Create a custom error for these.
cl_id: str = config["CLIENT_ID"] or ""
cl_secret: str = config["CLIENT_SECRET"] or ""

if not (cl_id and cl_secret):
    raise Exception("Missing env vars. Please check the .env file on project root.")

app = FastAPI()
app.include_router(auth_url.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

'''
from .schemas.pkce import PKCEItemCreate
pkce_dict = {"state": "wisemensay", "code_verifier": "onlyfoolsrushin"} 
pkce.non_endpoint_create_pkce(PKCEItemCreate(**pkce_dict))

pkce_dict2 = {"state": "buticanthelp", "code_verifier": "fallinginlovewithyou"} 
pkce.non_endpoint_create_pkce(PKCEItemCreate(**pkce_dict2))

# This works, despite the error.
print(pkce.non_endpoint_find_state("dela").code_verifier) 
'''

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)

@app.get("/callback")
async def callback(code: str, state: str):
    '''
    The callback looks for the received state in the on-disk database.
    If it finds the state, it gets the associated code_verifier.
    The code verifier is then used to compose the request to get
    the access and refresh tokens.

    The following are what's needed to make the token request:

        For the authorization header:
            "Basic " + base64encode(client_id + ":" + client_secret)

        client_id ( sourced from .env )
        auth_code ( the authentication code )
        code_verifier

    Please refer heavily to this doc:
    https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/oauth2-tutorial/?clientEncodedId=238N67&redirectUri=https://johanns.xyz/fitbitapp/callback&applicationType=SERVER
    '''
    resp_str = f"CODE = {code}, STATE = {state}"

    client_id: str = cl_id
    client_secret: str = cl_secret

    basic_token: str = client_id + ":" + client_secret

    authorization_header: str = f"Basic {base64.b64encode(basic_token.encode('utf-8')).decode('utf-8')}"
    auth_code: str = code
    code_verifier: str = pkce.non_endpoint_find_state(state).code_verifier # type: ignore


    return {"Response": resp_str}
