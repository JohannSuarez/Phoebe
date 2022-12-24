from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth_url
from dotenv import dotenv_values

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

@app.get("/callback")
async def callback(code: str, state: str):
    resp_str = f"CODE = {code}, STATE = {state}"
    return {"Response": resp_str}
