from .utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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


create_tables()

config = dotenv_values(".env")
# These variables have to be checked otherwise, we raise an Exception
# because the app is useless without these.
# Create a custom error for these.
client_id: str = config["CLIENT_ID"] or ""
client_secret: str = config["CLIENT_SECRET"] or ""

if not (client_id and client_secret):
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

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)

app.include_router(pkce.router)

@app.get("/callback")
async def callback(code: str, state: str):
    resp_str = f"CODE = {code}, STATE = {state}"
    return {"Response": resp_str}
