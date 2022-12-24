from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth_url

app = FastAPI()

app.include_router(auth_url.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post("/callback/")
async def callback(code: str, state: str):
    resp_str = f"CODE = {code}, STATE = {state}"
    return {"Response": resp_str}
