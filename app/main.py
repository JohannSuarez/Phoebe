from fastapi import FastAPI, Request
from .routers import auth_url


app = FastAPI()
app.include_router(auth_url.router)

callback_response: dict = {"message": "Lise"}

@app.post("/callback/")
async def callback(code: str):
    resp_str = f"You sent {code}"
    return {"Response": resp_str}
