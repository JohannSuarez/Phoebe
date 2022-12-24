from fastapi import FastAPI, Request
from .routers import auth_url


app = FastAPI()
app.include_router(auth_url.router)

@app.post("/callback/")
async def callback(code: str, state: str):
    resp_str = f"CODE = {code}, STATE = {state}"
    return {"Response": resp_str}
